from typing import Self, Literal

from domain.enums import GameEvent
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameFinishPayload(BasePayload):
    text: str


class GameFinish(BaseMessage):
    event: Literal[GameEvent.GAME_FINISH] = GameEvent.GAME_FINISH
    payload: GameFinishPayload

    @classmethod
    def create(cls, text: str) -> Self:
        return cls(payload=GameFinishPayload(text=text))
