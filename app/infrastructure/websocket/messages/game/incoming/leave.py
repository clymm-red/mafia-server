from typing import Literal

from domain.enums import GameAction
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class LeavePayload(BasePayload):
    room_id: str


class Leave(BaseMessage):
    action: Literal[GameAction.LEAVE] = GameAction.LEAVE
    payload: LeavePayload
