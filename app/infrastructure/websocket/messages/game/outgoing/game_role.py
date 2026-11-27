from typing import Self, Literal

from domain.enums import RoleEnum, MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameRolePayload(BasePayload):
    text: str
    role: RoleEnum


class GameRole(BaseMessage):
    message_type: Literal[MessageType.ROLE] = MessageType.ROLE
    payload: GameRolePayload

    @classmethod
    def create(cls, text: str, role: RoleEnum) -> Self:
        return cls(payload=GameRolePayload(text=text, role=role))
