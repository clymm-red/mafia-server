from typing import Literal

from domain.enums import Topic, MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameErrorPayload(BasePayload):
    text: str


class GameError(BaseMessage):
    message_type: Literal[MessageType.ERROR] = MessageType.ERROR
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameErrorPayload
