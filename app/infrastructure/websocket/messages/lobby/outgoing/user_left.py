from typing import Literal

from domain.enums import Topic, WebSocketMessageTypeEnum
from presentation.http.v1.responses import UserResponse, LobbyResponse
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class UserLeftPayload(BasePayload):
    text: str
    user: UserResponse
    lobby: LobbyResponse | None


class UserLeft(BaseMessage):
    message_type: Literal[WebSocketMessageTypeEnum.USER_LEAVE] = (
        WebSocketMessageTypeEnum.USER_LEAVE
    )
    topic: Topic
    payload: UserLeftPayload
