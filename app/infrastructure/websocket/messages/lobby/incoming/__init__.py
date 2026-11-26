from typing import Annotated

from pydantic import Field, TypeAdapter

from infrastructure.websocket.messages.lobby.incoming.kick_user import (
    KickUser,
    KickUserPayload,
)
from infrastructure.websocket.messages.lobby.incoming.start_game import (
    StartGame,
    StartGamePayload,
)
from infrastructure.websocket.messages.lobby.incoming.leave_lobby import (
    LeaveLobby,
    LeaveLobbyPayload,
)
from infrastructure.websocket.messages.lobby.incoming.delete_lobby import (
    DeleteLobby,
    DeleteLobbyPayload,
)


IncomingLobbyMessage = DeleteLobby | KickUser | LeaveLobby | StartGame

LobbyAdapter = TypeAdapter(
    Annotated[IncomingLobbyMessage, Field(discriminator="action")]
)


__all__ = [
    "DeleteLobby",
    "DeleteLobbyPayload",
    "IncomingLobbyMessage",
    "KickUser",
    "KickUserPayload",
    "LeaveLobby",
    "LeaveLobbyPayload",
    "LobbyAdapter",
    "StartGame",
    "StartGamePayload",
]
