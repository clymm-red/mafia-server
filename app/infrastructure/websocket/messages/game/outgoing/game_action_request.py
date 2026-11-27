from typing import Literal

from domain.enums import Topic, MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameActionRequestPayload(BasePayload):
    text: str
    timeout: int


class GameActionRequest(BaseMessage):
    message_type: Literal[MessageType.ACTION_REQUEST] = (
        MessageType.ACTION_REQUEST
    )
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameActionRequestPayload
