from .game_data import GameData
from .game_info import GameInfo
from .game_role import GameRole
from .game_error import GameError
from .game_event import GameEvent
from .game_start import GameStart
from .game_finish import GameFinish
from .game_new_stage import GameNewStage
from .game_action_request import GameActionRequest


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
    "GameData",
    "GameError",
    "GameEvent",
    "GameFinish",
    "GameInfo",
    "GameNewStage",
    "GameRole",
    "GameStart",
    "OutgoingGameMessage",
]
