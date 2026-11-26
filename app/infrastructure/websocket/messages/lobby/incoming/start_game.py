from typing import Literal

from domain.enums import RoleEnum, LobbyAction
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class StartGamePayload(BasePayload):
    room_id: str
    role_set: list[RoleEnum]


class StartGame(BaseMessage):
    action: Literal[LobbyAction.START] = LobbyAction.START
    payload: StartGamePayload
