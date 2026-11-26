from uuid import UUID

from dishka import FromDishka

from domain.enums import (
    LobbyCommandType,
    WebSocketTopicEnum,
    WebSocketMessageTypeEnum,
)
from domain.exceptions import DomainException, RoomNotFoundException
from application.commands import LobbyLeaveCommand
from application.services import GameService, GameManagerService
from infrastructure.logger import get_logger
from infrastructure.websocket import WebSocketManager
from presentation.http.v1.requests import CurrentUser
from infrastructure.redis.repositories import LobbyRepository
from infrastructure.websocket.messages import (
    WebSocketMessage,
    LobbyCommandPayload,
)
from application.services.lobby_service import LobbyService


logger = get_logger(f"{__name__}.LobbyWebSockeMessageHandler")


class LobbyMessageHandler:
    def __init__(
        self,
        game_service: FromDishka[GameService],
        lobby_service: FromDishka[LobbyService],
        lobby_repository: FromDishka[LobbyRepository],
        game_manager: FromDishka[GameManagerService],
        notification_service: FromDishka[WebSocketManager],
        websocket_manager: FromDishka[WebSocketManager],
    ):
        self._game_service = game_service
        self._lobby_service = lobby_service
        self._lobby_repository = lobby_repository
        self._notification_service = notification_service
        self._game_manager = game_manager
        self._websocket_manager = websocket_manager

    async def handle(
        self, message: WebSocketMessage, current_user: CurrentUser
    ):
        """
        Обрабатывает Lobby Websocket Message взависимости от его типа
        """
        logger.debug("handle")
        logger.debug(message.model_dump_json())

        if message.message_type == WebSocketMessageTypeEnum.COMMAND:
            payload = LobbyCommandPayload(**message.payload.model_dump())

            match payload.action_type:
                case LobbyCommandType.START:
                    await self.__handle_start(payload)
                case LobbyCommandType.KICK:
                    await self.__handle_kick(payload)
                case LobbyCommandType.DELETE:
                    await self.__handle_delete(payload, current_user.id)
                case LobbyCommandType.LEAVE:
                    await self.__handle_leave(payload, current_user.id)

    async def __handle_start(self, payload: LobbyCommandPayload):
        if not payload.role_set:
            exc = DomainException(
                WebSocketTopicEnum.LOBBY,
                "WebsSocketCommand missing role_set",
            )
            logger.error(exc)
            raise exc

        lobby = await self._lobby_repository.get_lobby_by_id(payload.room_id)

        if not lobby:
            exc = RoomNotFoundException(context_id=payload.room_id)
            logger.error(exc)
            raise exc

        logger.debug("calling create game")
        new_game = await self._game_service.create_game_from_lobby(
            lobby, payload.role_set
        )
        logger.debug("calling start game")
        await self._game_manager.start_game(new_game)

    async def __handle_kick(self, payload: LobbyCommandPayload):
        if not payload.target_id:
            exc = DomainException(
                WebSocketTopicEnum.LOBBY,
                "WebSocket KICK command missing target_id",
            )
            logger.error(exc)
            raise exc

        lobby_leave_command = LobbyLeaveCommand(
            lobby_id=payload.room_id,
            user_id=payload.target_id,
        )

        await self._lobby_service.leave_lobby(lobby_leave_command)
        await self._websocket_manager.disconnect(
            lobby_leave_command.lobby_id,
            lobby_leave_command.user_id,
        )

    async def __handle_delete(
        self, payload: LobbyCommandPayload, user_id: UUID
    ):
        lobby_leave_command = LobbyLeaveCommand(
            lobby_id=payload.room_id,
            user_id=user_id,
        )
        await self._lobby_service.leave_lobby(lobby_leave_command)
        await self._websocket_manager.delete_all_connections(
            lobby_leave_command.lobby_id
        )

    async def __handle_leave(self, payload: LobbyCommandPayload, user_id: UUID):
        lobby_leave_command = LobbyLeaveCommand(
            lobby_id=payload.room_id,
            user_id=user_id,
        )
        await self._lobby_service.leave_lobby(lobby_leave_command)
        await self._websocket_manager.disconnect(
            lobby_leave_command.lobby_id,
            lobby_leave_command.user_id,
        )
