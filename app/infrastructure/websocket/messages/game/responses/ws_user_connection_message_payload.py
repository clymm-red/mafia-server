from presentation.http.v1.responses import UserResponse, LobbyResponse
from infrastructure.websocket.messages.base_payload import BasePayload


class WSUserConnectionMessagePayload(BasePayload):
    text: str
    user: UserResponse
    lobby: LobbyResponse | None
