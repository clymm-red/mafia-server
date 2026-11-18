from uuid import UUID
from dataclasses import dataclass


@dataclass
class GameCommand:
    actor_id: UUID
    room_id: str
    target_id: UUID | None = None
