from typing import Literal

from domain.enums import Topic
from infrastructure.websocket.messages.base_message import BaseMessage


class LobbyMessage(BaseMessage):
    topic: Literal[Topic.LOBBY] = Topic.LOBBY
