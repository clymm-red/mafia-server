from uuid import UUID

from domain.enums import RoleEnum, LobbyCommandType
from infrastructure.websocket.messages.base_payload import BasePayload


class LobbyCommandPayload(BasePayload):
    action_type: LobbyCommandType
    target_id: UUID | None
    room_id: str
    role_set: list[RoleEnum] | None
