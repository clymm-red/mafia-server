from uuid import UUID

from presentation.http.v1.responses.user_response import UserResponse
from infrastructure.websocket.messages.base_payload import BasePayload


class WSLobbyDataPayload(BasePayload):
    id: str
    participants: list[UserResponse]
    admin_id: UUID
    max_players: int
