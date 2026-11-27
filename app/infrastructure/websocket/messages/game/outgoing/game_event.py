from typing import Self, Literal

from domain.enums import GameEvent as GameEventEnum
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameEventPayload(BasePayload):
    text: str


class GameEvent(BaseMessage):
    event: Literal[GameEventEnum.EVENT] = GameEventEnum.EVENT
    payload: GameEventPayload

    @classmethod
    def create(cls, text: str) -> Self:
        return cls(payload=GameEventPayload(text=text))
