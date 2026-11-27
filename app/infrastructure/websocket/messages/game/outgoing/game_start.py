from typing import Literal

from domain.enums import Topic, MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameStartPayload(BasePayload):
    text: str


class GameStart(BaseMessage):
    message_type: Literal[MessageType.GAME_START] = MessageType.GAME_START
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameStartPayload
