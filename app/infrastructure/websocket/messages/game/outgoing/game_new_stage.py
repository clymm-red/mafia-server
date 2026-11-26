from typing import Literal

from domain.enums import Topic, GameStageEnum, WebSocketMessageTypeEnum
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameNewStagePayload(BasePayload):
    new_stage: GameStageEnum
    text: str


class GameNewStage(BaseMessage):
    message_type: Literal[WebSocketMessageTypeEnum.NEW_STAGE] = (
        WebSocketMessageTypeEnum.NEW_STAGE
    )
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameNewStagePayload
