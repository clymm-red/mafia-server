from uuid import UUID

from domain.enums import WebSocketGameCommandActionTypeEnum
from infrastructure.websocket.messages.base_websocket_message import (
    BaseWebSocketMessage,
)


class WSGameCommandPayload(BaseWebSocketMessage):
    action_type: WebSocketGameCommandActionTypeEnum
    actor_id: UUID
    target_id: UUID | None
    room_id: str
