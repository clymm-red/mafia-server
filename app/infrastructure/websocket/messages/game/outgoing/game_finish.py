from typing import Literal

from domain.enums import Topic, WebSocketMessageTypeEnum
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameFinishPayload(BasePayload):
    text: str


class GameFinish(BaseMessage):
    message_type: Literal[WebSocketMessageTypeEnum.GAME_FINISH] = (
        WebSocketMessageTypeEnum.GAME_FINISH
    )
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameFinishPayload
