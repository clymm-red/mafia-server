from typing import Literal

from domain.enums import Topic, WebSocketMessageTypeEnum
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class LobbyErrorPayload(BasePayload):
    text: str


class LobbyError(BaseMessage):
    message_type: Literal[WebSocketMessageTypeEnum.ERROR] = (
        WebSocketMessageTypeEnum.ERROR
    )
    topic: Literal[Topic.LOBBY] = Topic.LOBBY
    payload: LobbyErrorPayload
