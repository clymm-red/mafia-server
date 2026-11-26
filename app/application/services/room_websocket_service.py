from datetime import datetime

from dishka import FromDishka
from fastapi import WebSocket

from domain.enums import Topic, WebSocketMessageTypeEnum
from application.commands import LobbyJoinCommand
from application.services import UserService, LobbyService
from infrastructure.logger import get_logger
from infrastructure.websocket import WebSocketManager
from presentation.http.v1.requests import CurrentUser
from presentation.http.v1.responses import UserResponse, LobbyResponse
from application.ws_message_handlers import (
    LobbyMessageHandler,
    GameWSMessageHandler,
)
from infrastructure.websocket.messages import (
    WebSocketMessage,
    WSUserConnectionMessagePayload,
)
from infrastructure.websocket.messages.unknown_message import UnknownMessage


logger = get_logger(f"{__name__}.RoomWebSocketService")


class RoomWebSocketService:
    def __init__(
        self,
        websocket_manager: FromDishka[WebSocketManager],
        game_websocket_handler: FromDishka[GameWSMessageHandler],
        lobby_websocket_handler: FromDishka[LobbyMessageHandler],
        user_service: FromDishka[UserService],
        lobby_service: FromDishka[LobbyService],
    ):
        self._websocket_manager = websocket_manager
        self._game_handler = game_websocket_handler
        self._lobby_handler = lobby_websocket_handler
        self._user_service = user_service
        self._lobby_service = lobby_service

    async def subscribe_room_webscoket(
        self, room_id: str, current_user: CurrentUser, websocket: WebSocket
    ):
        logger.debug("subscribe_room_webscoket")
        await self._websocket_manager.connect(
            websocket, room_id, current_user.id
        )

        lobby: LobbyResponse = await self._lobby_service.join_lobby(
            LobbyJoinCommand(room_id, current_user.id)
        )

        message = WebSocketMessage(
            message_type=WebSocketMessageTypeEnum.USER_CONNECT,
            topic=Topic.LOBBY if lobby else Topic.GAME,
            timestamp=datetime.now().isoformat(),
            payload=WSUserConnectionMessagePayload(
                text=f"User {current_user.username} подключился к комнате",
                user=UserResponse(
                    id=current_user.id,
                    name=current_user.username,
                    email=current_user.email,
                ),
                lobby=lobby if lobby else None,
            ),
        )
        await self._websocket_manager.send_broadcast(message, room_id)

    async def unsubscribe_room_webscoket(
        self, room_id: str, current_user: CurrentUser
    ):
        logger.debug("unsubscribe_room_webscoket")
        await self._websocket_manager.handle_disconnect(
            room_id, current_user.id
        )

        user_joined_room = await self._user_service.get_user_joined_room(
            current_user.id
        )
        if not user_joined_room:
            logger.error("Can't unsubscribe non-existing room")
            return

        # logger.info("leave ")
        # await self._lobby_service.leave_lobby(
        #     LobbyLeaveCommand(
        #         lobby_id=room_id,
        #         user_id=current_user.id,
        #     )
        # )

        message = WebSocketMessage(
            message_type=WebSocketMessageTypeEnum.USER_LEAVE,
            topic=(Topic.LOBBY if user_joined_room.is_lobby else Topic.GAME),
            timestamp=datetime.now().isoformat(),
            payload=WSUserConnectionMessagePayload(
                text=f"User {current_user.username} покинул комнату",
                user=UserResponse(
                    id=current_user.id,
                    name=current_user.username,
                    email=current_user.email,
                ),
                lobby=None,
            ),
        )
        await self._websocket_manager.send_broadcast(message, room_id)

    async def handle_message(
        self,
        old_message: WebSocketMessage | None,
        message: UnknownMessage,
        current_user: CurrentUser,
    ):
        logger.debug("handle_message")

        match message.topic:
            case Topic.LOBBY:
                lobby_message = message.to_lobby_message()
                await self._lobby_handler.handle(lobby_message, current_user)
            case Topic.GAME:
                assert old_message is not None
                await self._game_handler.handle(old_message, current_user)
            case _:
                raise TypeError("Что-то тут не так")
