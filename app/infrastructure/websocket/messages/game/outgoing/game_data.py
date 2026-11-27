from uuid import UUID
from typing import Self, Literal
from datetime import datetime

from domain.enums import (
    RoleEnum,
    TeamEnum,
    GameEvent,
    GameStage,
    GameStatusEnum,
)
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload


class GamePlayerPayload(BasePayload):
    id: UUID
    name: str
    email: str
    is_alive: bool


class GameDataPayload(BasePayload):
    id: str
    players: list[GamePlayerPayload]
    admin: GamePlayerPayload

    start_date: datetime
    assigned_role: RoleEnum

    winner_team: TeamEnum | None
    game_status: GameStatusEnum
    game_stage: GameStage
    finish_date: datetime | None
    round_count: int


class GameData(BaseMessage):
    event: Literal[GameEvent.GAME_DATA] = GameEvent.GAME_DATA
    payload: GameDataPayload

    @classmethod
    def create(
        cls,
        id: str,
        players: list[GamePlayerPayload],
        admin: GamePlayerPayload,
        start_date: datetime,
        assigned_role: RoleEnum,
        winner_team: TeamEnum | None,
        game_status: GameStatusEnum,
        game_stage: GameStage,
        finish_date: datetime | None,
        round_count: int,
    ) -> Self:
        return cls(
            payload=GameDataPayload(
                id=id,
                players=players,
                admin=admin,
                start_date=start_date,
                assigned_role=assigned_role,
                winner_team=winner_team,
                game_status=game_status,
                game_stage=game_stage,
                finish_date=finish_date,
                round_count=round_count,
            )
        )
