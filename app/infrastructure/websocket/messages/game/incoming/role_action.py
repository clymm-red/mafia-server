from uuid import UUID
from typing import Literal

from domain.enums import GameAction
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class RoleActionPayload(BasePayload):
    room_id: str
    target_id: UUID | None


class RoleAction(BaseMessage):
    action: Literal[GameAction.ROLE_ACTION] = GameAction.ROLE_ACTION
    payload: RoleActionPayload
