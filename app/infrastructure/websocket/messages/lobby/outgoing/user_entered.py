from uuid import UUID
from typing import Self, Literal

from domain.enums import LobbyEvent
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class UserEnteredPayload(BasePayload):
    id: UUID
    name: str


class UserEntered(BaseMessage):
    event: Literal[LobbyEvent.USER_CONNECT] = LobbyEvent.USER_CONNECT
    payload: UserEnteredPayload

    @classmethod
    def create(cls, id: UUID, name: str) -> Self:
        return cls(payload=UserEnteredPayload(id=id, name=name))
