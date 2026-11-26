from typing import Annotated

from pydantic import Field, TypeAdapter

from .kick_user import KickUser, KickUserPayload
from .start_game import StartGame, StartGamePayload
from .leave_lobby import LeaveLobby, LeaveLobbyPayload
from .delete_lobby import DeleteLobby, DeleteLobbyPayload


IncomingLobbyMessage = DeleteLobby | KickUser | LeaveLobby | StartGame
LobbyMessageAdapter = TypeAdapter(
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
    "LobbyMessageAdapter",
    "StartGame",
    "StartGamePayload",
]
