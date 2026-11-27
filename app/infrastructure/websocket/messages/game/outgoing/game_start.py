from typing import Self, Literal

from domain.enums import MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameStartPayload(BasePayload):
    text: str


class GameStart(BaseMessage):
    message_type: Literal[MessageType.GAME_START] = MessageType.GAME_START
    payload: GameStartPayload

    @classmethod
    def create(cls, text: str) -> Self:
        return cls(payload=GameStartPayload(text=text))
