from typing import Literal

from domain.enums import LobbyAction
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class DeleteLobbyPayload(BasePayload):
    room_id: str


class DeleteLobby(BaseMessage):
    action: Literal[LobbyAction.DELETE] = LobbyAction.DELETE
    payload: DeleteLobbyPayload
