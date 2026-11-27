from typing import Any, Self

from pydantic import ConfigDict, ValidationError

from domain.enums import Topic
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.game.incoming import (
    GameMessageAdapter,
    IncomingGameMessage,
)
from infrastructure.websocket.messages.lobby.incoming import (
    LobbyMessageAdapter,
    IncomingLobbyMessage,
)


class IncomingMessage(BaseMessage):
    """Тип сообщения в который превращается словарь"""

    topic: Topic

    model_config = ConfigDict(extra="allow")

    @classmethod
    def from_dict(cls, dict: dict[str, Any]) -> Self | None:
        try:
            return cls.model_validate(dict)
        except ValidationError:
            return None

    def to_lobby_message(self) -> IncomingLobbyMessage:
        extra = self.__pydantic_extra__
        return LobbyMessageAdapter.validate_python(extra)

    def to_game_message(self) -> IncomingGameMessage:
        extra = self.__pydantic_extra__
        return GameMessageAdapter.validate_python(extra)
