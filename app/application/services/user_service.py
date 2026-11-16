from uuid import UUID

from dishka import FromDishka
from fastapi import UploadFile

from infrastructure.logger_config import get_logger
from infrastructure.redis.repositories import GameRepository, LobbyRepository
from application.services.avatar_service import AvatarService
from infrastructure.database.repositories import UserRepository
from presentation.api.v1.dtos.responses.room_response import RoomResponse


logger = get_logger(f"{__name__}.UserService")


class UserService:
    def __init__(
        self,
        user_repository: FromDishka[UserRepository],
        lobby_repository: FromDishka[LobbyRepository],
        game_repository: FromDishka[GameRepository],
        avatar_service: FromDishka[AvatarService],
    ):
        self._user_repository = user_repository
        self._lobby_repository = lobby_repository
        self._game_repository = game_repository
        self._avatar_service = avatar_service

    async def get_user_joined_room(self, user_id: UUID) -> RoomResponse | None:
        logger.debug("get_user_joined_room")
        room_id = await self._lobby_repository.get_user_active_room_id(user_id)
        if not room_id:
            return None
        lobby = await self._lobby_repository.get_lobby_by_id(room_id)

        return RoomResponse(room_id=room_id, is_lobby=bool(lobby))

    async def get_user_avatar(self, user_id: UUID) -> bytes | None:
        return await self._avatar_service.get_user_avatar(user_id)

    async def set_user_avatar(self, user_id: UUID, file: UploadFile) -> bool:
        return await self._avatar_service.set_user_avatar(user_id, file)
