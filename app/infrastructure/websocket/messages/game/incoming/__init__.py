from typing import Annotated

from pydantic import Field, TypeAdapter

from .vote import Vote, VotePayload
from .leave import Leave, LeavePayload
from .end_talk import EndTalk, EndTalkPayload
from .role_action import RoleAction, RoleActionPayload


IncomingGameMessage = Vote | RoleAction | EndTalk | Leave
GameMessageAdapter = TypeAdapter(
    Annotated[IncomingGameMessage, Field(discriminator="action")]
)

__all__ = [
    "EndTalk",
    "EndTalkPayload",
    "GameMessageAdapter",
    "IncomingGameMessage",
    "Leave",
    "LeavePayload",
    "RoleAction",
    "RoleActionPayload",
    "Vote",
    "VotePayload",
]
