from typing import Literal

from domain.enums import Topic, MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameFinishPayload(BasePayload):
    text: str


class GameFinish(BaseMessage):
    message_type: Literal[MessageType.GAME_FINISH] = MessageType.GAME_FINISH
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameFinishPayload
