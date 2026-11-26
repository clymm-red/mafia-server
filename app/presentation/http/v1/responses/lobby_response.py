from uuid import UUID

from presentation.http.base_dto import BaseDTO
from presentation.http.v1.responses import UserResponse


class LobbyResponse(BaseDTO):
    status: str
    id: str
    admin_id: UUID
    max_players: int
    participants: list[UserResponse]
