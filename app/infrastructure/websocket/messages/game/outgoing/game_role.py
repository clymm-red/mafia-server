from typing import Self, Literal

from domain.enums import RoleEnum, GameEvent
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameRolePayload(BasePayload):
    text: str
    role: RoleEnum


class GameRole(BaseMessage):
    event: Literal[GameEvent.ROLE] = GameEvent.ROLE
    payload: GameRolePayload

    @classmethod
    def create(cls, text: str, role: RoleEnum) -> Self:
        return cls(payload=GameRolePayload(text=text, role=role))
