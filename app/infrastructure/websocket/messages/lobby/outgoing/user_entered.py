from uuid import UUID
from typing import Self, Literal

from domain.enums import MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class UserEnteredPayload(BasePayload):
    id: UUID
    name: str


class UserEntered(BaseMessage):
    message_type: Literal[MessageType.USER_CONNECT] = MessageType.USER_CONNECT
    payload: UserEnteredPayload

    @classmethod
    def create(cls, id: UUID, name: str) -> Self:
        return cls(payload=UserEnteredPayload(id=id, name=name))
