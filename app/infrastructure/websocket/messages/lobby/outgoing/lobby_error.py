from typing import Self, Literal

from domain.enums import MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class LobbyErrorPayload(BasePayload):
    text: str


class LobbyError(BaseMessage):
    message_type: Literal[MessageType.ERROR] = MessageType.ERROR
    payload: LobbyErrorPayload

    @classmethod
    def create(cls, text: str) -> Self:
        return cls(payload=LobbyErrorPayload(text=text))
