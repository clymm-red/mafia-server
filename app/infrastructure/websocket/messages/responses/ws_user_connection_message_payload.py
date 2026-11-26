from presentation.http.v1.responses import UserResponse, LobbyResponse
from infrastructure.websocket.messages.base_websocket_message import (
    BaseWebSocketMessage,
)


class WSUserConnectionMessagePayload(BaseWebSocketMessage):
    text: str
    user: UserResponse
    lobby: LobbyResponse | None
