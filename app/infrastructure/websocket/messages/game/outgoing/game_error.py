from typing import Self, Literal

from domain.enums import GameEvent
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameErrorPayload(BasePayload):
    text: str


class GameError(BaseMessage):
    event: Literal[GameEvent.ERROR] = GameEvent.ERROR
    payload: GameErrorPayload

    @classmethod
    def create(cls, text: str) -> Self:
        return cls(payload=GameErrorPayload(text=text))
