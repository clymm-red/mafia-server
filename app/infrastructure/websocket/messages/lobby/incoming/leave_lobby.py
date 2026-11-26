from typing import Literal

from domain.enums import LobbyAction
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class LeaveLobbyPayload(BasePayload):
    room_id: str


class LeaveLobby(BaseMessage):
    action: Literal[LobbyAction.LEAVE] = LobbyAction.LEAVE
    payload: LeaveLobbyPayload
