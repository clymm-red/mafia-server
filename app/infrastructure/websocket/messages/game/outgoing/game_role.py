from typing import Literal

from domain.enums import Topic, RoleEnum, MessageType
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameRolePayload(BasePayload):
    text: str
    role: RoleEnum


class GameRole(BaseMessage):
    message_type: Literal[MessageType.ROLE] = MessageType.ROLE
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameRolePayload
