from infrastructure.websocket.messages.base_websocket_message import (
    BaseWebSocketMessage,
)


class WSGameActionRequestPayload(BaseWebSocketMessage):
    text: str
    timeout: int
