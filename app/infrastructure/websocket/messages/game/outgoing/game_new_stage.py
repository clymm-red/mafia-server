from typing import Self, Literal

from domain.enums import MessageType, GameStageEnum
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameNewStagePayload(BasePayload):
    new_stage: GameStageEnum
    text: str


class GameNewStage(BaseMessage):
    message_type: Literal[MessageType.NEW_STAGE] = MessageType.NEW_STAGE
    payload: GameNewStagePayload

    @classmethod
    def create(cls, new_stage: GameStageEnum, text: str) -> Self:
        return cls(payload=GameNewStagePayload(new_stage=new_stage, text=text))
