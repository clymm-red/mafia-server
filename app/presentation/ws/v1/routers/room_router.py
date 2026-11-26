from typing import Any

from dishka import FromDishka, AsyncContainer
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter
from starlette.websockets import WebSocketState
from dishka.integrations.fastapi import inject

from domain.enums import Topic
from domain.exceptions import DomainException
from application.services import SecurityService, RoomWebSocketService
from infrastructure.logger import get_logger
from presentation.http.v1.requests import CurrentUser
from infrastructure.websocket.messages import (
    GameError,
    LobbyError,
    GameErrorPayload,
    LobbyErrorPayload,
)
from infrastructure.websocket.messages.unknown_message import UnknownMessage


room_router = APIRouter()
logger = get_logger(__name__, 10)


@room_router.websocket("/rooms/{room_id}")
@inject
async def room_websocket(
    room_id: str, websocket: WebSocket, container: FromDishka[AsyncContainer]
):
    logger.debug("room_websocket")
    token = _extract_token(websocket)

    current_user = None
    subscribed = False

    try:
        async with container() as request_container:
            security_service = await request_container.get(SecurityService)
            current_user = await security_service.get_current_user(token)

        async with container() as request_container:
            room_websocket_service = await request_container.get(
                RoomWebSocketService
            )
            await room_websocket_service.subscribe_room_webscoket(
                room_id, current_user, websocket
            )

        subscribed = True
        await _listen_websocket_messages(websocket, container, current_user)
    except WebSocketDisconnect:
        username = current_user.username if current_user else ""
        logger.info(f"{username} разорвал соединение с комнатой {room_id}")
    finally:
        # Очистка должна выполняться при любом выходе (disconnect,
        # отмена задачи, исключение во время подписки), иначе
        # лобби/участники остаются в Redis.
        if subscribed and current_user is not None:
            try:
                async with container() as request_container:
                    room_service = await request_container.get(
                        RoomWebSocketService
                    )
                    await room_service.unsubscribe_room_webscoket(
                        room_id, current_user
                    )
            except Exception as e:
                logger.error(f"Error on unsubscribe: {e.args}")


def _extract_token(websocket):
    token = websocket.headers.get("authorization", "").removeprefix("Bearer ")

    if not token:
        token = websocket.query_params.get("authorization", "").removeprefix(
            "Bearer "
        )
    return token


async def _listen_websocket_messages(
    websocket: WebSocket,
    container: FromDishka[AsyncContainer],
    current_user: CurrentUser,
):
    while websocket.application_state == WebSocketState.CONNECTED:
        raw_message: dict[str, Any] = await websocket.receive_json()
        logger.debug(f"{raw_message} {type(raw_message)}")

        message = UnknownMessage.from_dict(raw_message)

        try:
            if message:
                await _handle_message(container, current_user, message)
        except DomainException as e:
            logger.error(
                f"Error on handling message: {raw_message}\nError: {e.args}"
            )
            match e.topic:
                case Topic.LOBBY:
                    error = LobbyError(
                        payload=LobbyErrorPayload(text=e.message)
                    )
                case Topic.GAME:
                    error = GameError(payload=GameErrorPayload(text=e.message))
            await websocket.send_text(error.to_json())


async def _handle_message(
    container: FromDishka[AsyncContainer],
    current_user: CurrentUser,
    ws_message: UnknownMessage,
):
    async with container() as request_container:
        room_service = await request_container.get(RoomWebSocketService)
        await room_service.handle_message(ws_message, current_user)
