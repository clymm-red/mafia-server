from typing import Self, Literal

from domain.enums import MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameActionRequestPayload(BasePayload):
    text: str
    timeout: int


class GameActionRequest(BaseMessage):
    message_type: Literal[MessageType.ACTION_REQUEST] = (
        MessageType.ACTION_REQUEST
    )
    payload: GameActionRequestPayload

    @classmethod
    def create(cls, text: str, timeout: int) -> Self:
        return cls(payload=GameActionRequestPayload(text=text, timeout=timeout))
