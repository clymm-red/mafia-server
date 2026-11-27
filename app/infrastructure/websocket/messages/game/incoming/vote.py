from uuid import UUID
from typing import Literal

from domain.enums import GameAction
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class VotePayload(BasePayload):
    room_id: str
    target_id: UUID | None


class Vote(BaseMessage):
    action: Literal[GameAction.VOTE] = GameAction.VOTE
    payload: VotePayload
