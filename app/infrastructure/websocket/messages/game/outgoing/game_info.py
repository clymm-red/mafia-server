from typing import Self, Literal

from domain.enums import GameEvent
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameInfoPayload(BasePayload):
    text: str


class GameInfo(BaseMessage):
    event: Literal[GameEvent.INFO] = GameEvent.INFO
    payload: GameInfoPayload

    @classmethod
    def create(cls, text: str) -> Self:
        return cls(payload=GameInfoPayload(text=text))
