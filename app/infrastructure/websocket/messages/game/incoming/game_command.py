from uuid import UUID
from typing import Literal

from domain.enums import (
    Topic,
    WebSocketMessageTypeEnum,
    WebSocketGameCommandActionTypeEnum,
)
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GameCommandPayload(BasePayload):
    action_type: WebSocketGameCommandActionTypeEnum
    actor_id: UUID
    target_id: UUID | None
    room_id: str


class GameCommand(BaseMessage):
    message_type: Literal[WebSocketMessageTypeEnum.COMMAND] = (
        WebSocketMessageTypeEnum.COMMAND
    )
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameCommandPayload
