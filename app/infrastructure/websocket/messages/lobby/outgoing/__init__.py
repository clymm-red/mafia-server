from .user_left import UserLeft
from .lobby_error import LobbyError
from .user_entered import UserEntered


OutgoingLobbyMessage = UserEntered | UserLeft | LobbyError

__all__ = [
    "OutgoingLobbyMessage",
    "LobbyError",
    "UserEntered",
    "UserLeft",
]
