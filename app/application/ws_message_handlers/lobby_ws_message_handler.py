from uuid import UUID
from typing import assert_never

from dishka import FromDishka

from domain.exceptions import RoomNotFoundException
from application.services import GameService, GameManagerService
from infrastructure.logger import get_logger
from infrastructure.websocket import WebSocketManager
from presentation.http.v1.requests import CurrentUser
from infrastructure.redis.repositories import LobbyRepository
from application.services.lobby_service import LobbyService
from infrastructure.websocket.messages.lobby.incoming import (
    KickUserPayload,
    StartGamePayload,
    LeaveLobbyPayload,
    DeleteLobbyPayload,
    IncomingLobbyMessage,
)


logger = get_logger(f"{__name__}.LobbyWebSockeMessageHandler")


class LobbyMessageHandler:
    def __init__(
        self,
        game_service: FromDishka[GameService],
        lobby_service: FromDishka[LobbyService],
        lobby_repository: FromDishka[LobbyRepository],
        game_manager: FromDishka[GameManagerService],
        websocket_manager: FromDishka[WebSocketManager],
    ):
        self._game_service = game_service
        self._game_manager = game_manager
        self._lobby_service = lobby_service
        self._lobby_repository = lobby_repository
        self._websocket_manager = websocket_manager

    async def handle_message(
        self, message: IncomingLobbyMessage, current_user: CurrentUser
    ):
        """
        Обрабатывает Lobby Websocket Message взависимости от его типа
        """
        logger.debug("handle")
        logger.debug(message.to_json())

        payload = message.payload

        match payload:
            case StartGamePayload():
                await self.__start_game(payload)
            case KickUserPayload():
                await self.__kick_user(payload)
            case DeleteLobbyPayload():
                await self.__delete_lobby(payload, current_user.id)
            case LeaveLobbyPayload():
                await self.__leave_lobby(payload, current_user.id)
            case _:
                assert_never(payload)

    async def __start_game(self, payload: StartGamePayload):
        lobby_id = payload.room_id
        lobby = await self._lobby_repository.get_lobby_by_id(lobby_id)

        if not lobby:
            exc = RoomNotFoundException(context_id=lobby_id)
            logger.error(exc)
            raise exc

        logger.debug("calling create game")
        new_game = await self._game_service.create_game_from_lobby(
            lobby, payload.role_set
        )

        logger.debug("calling start game")
        await self._game_manager.start_game(new_game)

    async def __kick_user(self, payload: KickUserPayload):
        lobby_id = payload.room_id
        user_id = payload.target_id

        await self._lobby_service.leave_lobby(user_id, lobby_id)
        await self._websocket_manager.disconnect(lobby_id, user_id)

    async def __delete_lobby(self, payload: DeleteLobbyPayload, user_id: UUID):
        lobby_id = payload.room_id

        await self._lobby_service.leave_lobby(user_id, lobby_id)
        await self._websocket_manager.delete_all_connections(lobby_id)

    async def __leave_lobby(self, payload: LeaveLobbyPayload, user_id: UUID):
        lobby_id = payload.room_id

        await self._lobby_service.leave_lobby(user_id, lobby_id)
        await self._websocket_manager.disconnect(lobby_id, user_id)
