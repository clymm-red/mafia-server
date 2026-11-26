from typing import Literal

from domain.enums import Topic, WebSocketMessageTypeEnum
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameActionRequestPayload(BasePayload):
    text: str
    timeout: int


class GameActionRequest(BaseMessage):
    message_type: Literal[WebSocketMessageTypeEnum.ACTION_REQUEST] = (
        WebSocketMessageTypeEnum.ACTION_REQUEST
    )
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameActionRequestPayload
