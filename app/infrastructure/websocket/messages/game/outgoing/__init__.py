from .game_data import GameData, GameDataPayload, GamePlayerPayload
from .game_info import GameInfo, GameInfoPayload
from .game_role import GameRole, GameRolePayload
from .game_error import GameError, GameErrorPayload
from .game_event import GameEvent, GameEventPayload
from .game_start import GameStart, GameStartPayload
from .game_finish import GameFinish, GameFinishPayload
from .game_new_stage import GameNewStage, GameNewStagePayload
from .game_action_request import (
    GameActionRequest,
    GameActionRequestPayload,
)


OutgoingGameMessage = (
    GameStart
    | GameFinish
    | GameEvent
    | GameInfo
    | GameError
    | GameActionRequest
    | GameNewStage
    | GameRole
    | GameData
)

__all__ = [
    "GameActionRequest",
    "GameActionRequestPayload",
    "GameData",
    "GameDataPayload",
    "GameError",
    "GameErrorPayload",
    "GameEvent",
    "GameEventPayload",
    "GameFinish",
    "GameFinishPayload",
    "GameInfo",
    "GameInfoPayload",
    "GameNewStage",
    "GameNewStagePayload",
    "GamePlayerPayload",
    "GameRole",
    "GameRolePayload",
    "GameStart",
    "GameStartPayload",
    "OutgoingGameMessage",
]
