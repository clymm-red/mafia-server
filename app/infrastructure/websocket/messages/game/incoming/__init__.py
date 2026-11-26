from typing import Annotated

from pydantic import Field, TypeAdapter

from .game_command import GameCommand, GameCommandPayload


IncomingGameMessage = GameCommand
GameMessageAdapter = TypeAdapter(
    Annotated[IncomingGameMessage, Field(discriminator="message_type")]
)

__all__ = [
    "GameCommand",
    "GameCommandPayload",
    "GameMessageAdapter",
    "IncomingGameMessage",
]
