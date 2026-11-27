from typing import Self, Literal

from domain.enums import MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameFinishPayload(BasePayload):
    text: str


class GameFinish(BaseMessage):
    message_type: Literal[MessageType.GAME_FINISH] = MessageType.GAME_FINISH
    payload: GameFinishPayload

    @classmethod
    def create(cls, text: str) -> Self:
        return cls(payload=GameFinishPayload(text=text))
