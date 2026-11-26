from pydantic import ConfigDict

from domain.enums import Topic
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.lobby.incoming import (
    LobbyAdapter,
    IncomingLobbyMessage,
)


class UnknownMessage(BaseMessage):
    """Тип сообщения в который превращается словарь"""

    topic: Topic

    model_config = ConfigDict(extra="allow")

    def to_lobby_message(self) -> IncomingLobbyMessage:
        return LobbyAdapter.validate_python(self.__pydantic_extra__)

    def to_game_message(self):
        pass
