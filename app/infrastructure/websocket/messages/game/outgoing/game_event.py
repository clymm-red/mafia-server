from typing import Literal

from domain.enums import Topic, MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameEventPayload(BasePayload):
    text: str


class GameEvent(BaseMessage):
    message_type: Literal[MessageType.EVENT] = MessageType.EVENT
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameEventPayload
