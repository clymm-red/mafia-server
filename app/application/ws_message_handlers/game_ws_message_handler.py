from typing import assert_never

from dishka import FromDishka

from domain.enums import Topic, GameStage, GameAction
from domain.exceptions import DomainException, PlayerDisabledException
from application.services import GameService, GameManagerService
from infrastructure.logger import get_logger
from infrastructure.websocket import WebSocketManager
from presentation.http.v1.requests import CurrentUser
from infrastructure.websocket.messages import GameError
from infrastructure.websocket.messages.game.incoming import (
    VotePayload,
    LeavePayload,
    EndTalkPayload,
    RoleActionPayload,
    IncomingGameMessage,
)


logger = get_logger(f"{__name__}.GameWebSocketMessageHandler")


class GameWSMessageHandler:
    def __init__(
        self,
        game_service: FromDishka[GameService],
        game_manager: FromDishka[GameManagerService],
        websocket_manager: FromDishka[WebSocketManager],
    ):
        self._game_service = game_service
        self._game_manager = game_manager
        self._websocket_manager = websocket_manager

    async def handle_message(
        self, message: IncomingGameMessage, current_user: CurrentUser
    ):
        """
        Обрабатывает Game Websocket Message взависимости от его payload
        """
        logger.debug("handle")
        logger.debug(message.to_json())

        payload = message.payload

        match payload:
            case RoleActionPayload():
                await self.__process_role_action(payload, current_user)
            case VotePayload():
                await self.__process_vote(payload, current_user)
            case EndTalkPayload():
                await self.__end_talk(payload)
            case LeavePayload():
                await self.__leave(payload, current_user)
            case _:
                assert_never(payload)

    async def __process_role_action(
        self, payload: RoleActionPayload, current_user: CurrentUser
    ):
        game = await self._game_service.get_game_by_id(payload.room_id)

        try:
            if game.game_stage != GameStage.NIGHT:
                raise DomainException(Topic.GAME, "Неожиданное сообщение")

            result = await self._game_service.process_role_action(
                current_user.id, payload.room_id, payload.target_id
            )
        except DomainException as e:
            logger.info(
                f"Domain Exception from user {current_user.id} "
                f"in room {payload.room_id}: {e.args}"
            )
            await self._websocket_manager.send_to_one(
                GameError.create(text=e.message or "Неизвестная ошибка"),
                payload.room_id,
                current_user.id,
            )
            result = None

        await self._game_manager.set_event(
            payload.room_id,
            f"{GameAction.ROLE_ACTION}|"
            f"{result if isinstance(result, bool) else ''}",
        )

    async def __process_vote(
        self, payload: VotePayload, current_user: CurrentUser
    ):
        game = await self._game_service.get_game_by_id(payload.room_id)

        try:
            if game.game_stage != GameStage.DAY_VOTE:
                raise DomainException(Topic.GAME, "Неожиданное сообщение")

            await self._game_service.process_vote(
                current_user.id, payload.room_id, payload.target_id
            )
            target_id = str(payload.target_id)
        except DomainException as e:
            logger.info(
                f"Domain Exception from user {current_user.id} "
                f"in room {payload.room_id}: {e.args}"
            )
            await self._websocket_manager.send_to_one(
                GameError.create(text=e.message or "Неизвестная ошибка"),
                payload.room_id,
                current_user.id,
            )
            logger.debug("Сообщение об ошибке отправлено")
            if not isinstance(e, PlayerDisabledException):
                logger.debug("wait for another vote")
                return
            target_id = ""

        await self._game_manager.set_event(
            payload.room_id, f"{GameAction.VOTE}|{target_id}"
        )

    async def __end_talk(self, payload: EndTalkPayload):
        game = await self._game_service.get_game_by_id(payload.room_id)

        if game.game_stage in (
            GameStage.DAY_TALK,
            GameStage.DAY_INTRO,
        ):
            await self._game_manager.set_event(
                payload.room_id, GameAction.END_TALK
            )

    async def __leave(self, payload: LeavePayload, current_user: CurrentUser):
        await self._game_manager.set_event(
            payload.room_id,
            f"{GameAction.LEAVE}|{str(current_user.id)}",
        )
        await self._websocket_manager.disconnect(
            payload.room_id, current_user.id
        )
