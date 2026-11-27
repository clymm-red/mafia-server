from typing import Literal

from domain.enums import GameAction
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class EndTalkPayload(BasePayload):
    room_id: str


class EndTalk(BaseMessage):
    action: Literal[GameAction.END_TALK] = GameAction.END_TALK
    payload: EndTalkPayload
