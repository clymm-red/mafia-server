from typing import Literal
from datetime import datetime

from domain.enums import (
    Topic,
    RoleEnum,
    TeamEnum,
    GameStageEnum,
    GameStatusEnum,
    WebSocketMessageTypeEnum,
)
from infrastructure.websocket.messages.base_message import BaseMessage
from infrastructure.websocket.messages.base_payload import BasePayload
from presentation.http.v1.responses.player_response import PlayerResponse


class GameDataPayload(BasePayload):
    id: str
    players: list[PlayerResponse]
    admin: PlayerResponse

    start_date: datetime
    assigned_role: RoleEnum

    winner_team: TeamEnum | None
    game_status: GameStatusEnum
    game_stage: GameStageEnum
    finish_date: datetime | None
    round_count: int


class GameData(BaseMessage):
    message_type: Literal[WebSocketMessageTypeEnum.GAME_DATA] = (
        WebSocketMessageTypeEnum.GAME_DATA
    )
    topic: Literal[Topic.GAME] = Topic.GAME
    payload: GameDataPayload
