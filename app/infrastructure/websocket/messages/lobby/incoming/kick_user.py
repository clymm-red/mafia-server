from uuid import UUID
from typing import Literal

from domain.enums import LobbyAction
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class KickUserPayload(BasePayload):
    target_id: UUID
    room_id: str


class KickUser(BaseMessage):
    action: Literal[LobbyAction.KICK] = LobbyAction.KICK
    payload: KickUserPayload
