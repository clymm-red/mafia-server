from uuid import UUID
from typing import Self, Literal

from domain.enums import LobbyEvent
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class UserLeftPayload(BasePayload):
    id: UUID
    name: str


class UserLeft(BaseMessage):
    event: Literal[LobbyEvent.USER_LEAVE] = LobbyEvent.USER_LEAVE
    payload: UserLeftPayload

    @classmethod
    def create(cls, id: UUID, name: str) -> Self:
        return cls(payload=UserLeftPayload(id=id, name=name))
