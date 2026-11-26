from uuid import UUID

from domain.enums import RoleEnum, LobbyCommandType
from infrastructure.websocket.messages.base_websocket_message import (
    BaseWebSocketMessage,
)


class LobbyCommandPayload(BaseWebSocketMessage):
    action_type: LobbyCommandType
    target_id: UUID | None
    room_id: str
    role_set: list[RoleEnum] | None
