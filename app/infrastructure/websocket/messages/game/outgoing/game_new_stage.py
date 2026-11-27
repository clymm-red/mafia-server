from typing import Self, Literal

from domain.enums import GameEvent, GameStage
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameNewStagePayload(BasePayload):
    new_stage: GameStage
    text: str


class GameNewStage(BaseMessage):
    event: Literal[GameEvent.NEW_STAGE] = GameEvent.NEW_STAGE
    payload: GameNewStagePayload

    @classmethod
    def create(cls, new_stage: GameStage, text: str) -> Self:
        return cls(payload=GameNewStagePayload(new_stage=new_stage, text=text))
