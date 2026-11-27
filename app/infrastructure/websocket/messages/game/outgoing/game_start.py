from typing import Self, Literal

from domain.enums import GameEvent
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameStartPayload(BasePayload):
    text: str


class GameStart(BaseMessage):
    event: Literal[GameEvent.GAME_START] = GameEvent.GAME_START
    payload: GameStartPayload

    @classmethod
    def create(cls, text: str) -> Self:
        return cls(payload=GameStartPayload(text=text))
