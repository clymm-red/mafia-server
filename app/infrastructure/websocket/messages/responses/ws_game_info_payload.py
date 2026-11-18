from infrastructure.websocket.messages.base_websocket_message import (
    BaseWebSocketMessage,
)


class WSGameInfoPayload(BaseWebSocketMessage):
    text: str
