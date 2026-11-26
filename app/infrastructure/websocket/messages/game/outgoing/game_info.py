from typing import Literal

from domain.enums import Topic, WebSocketMessageTypeEnum
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameInfoPayload(BasePayload):
    text: str


class GameInfo(BaseMessage):
    message_type: Literal[WebSocketMessageTypeEnum.INFO] = (
        WebSocketMessageTypeEnum.INFO
    )
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameInfoPayload
