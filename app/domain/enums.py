from enum import StrEnum


class Topic(StrEnum):
    LOBBY = "Lobby"
    GAME = "Game"


class TeamEnum(StrEnum):
    NONE = "None"
    # Classic mode
    CITIZEN_TEAM = "CitizenTeam"
    MAFIA_TEAM = "MafiaTeam"

    # TODO Extended mode
    NEUTRAL = "Neutral"


class RoleEnum(StrEnum):
    # Sport mode
    CITIZEN = "Citizen"
    MAFIA_MEMBER = "MafiaMember"
    SHERIFF = "Sheriff"
    # Amateur mode
    DOCTOR = "Doctor"
    MAFIA_DON = "MafiaDon"
    PROSTITUTE = "Prostitute"
    # Extended mode
    MANIAC = "Maniac"
    DEPUTY_SHERIFF = "DeputySheriff"
    SHAPESHIFTER = "Shapeshifter"


class GameStatusEnum(StrEnum):
    IN_PROGRESS = "In progress"
    PAUSED = "Paused"
    FINISHED = "Finished"


class GameStage(StrEnum):
    DAY_INTRO = "DayIntro"
    DAY_TALK = "DayTalk"
    DAY_VOTE = "DayVote"
    NIGHT = "Night"


class GameAction(StrEnum):
    VOTE = "Vote"
    ROLE_ACTION = "RoleAction"
    END_TALK = "EndTalk"
    LEAVE = "Leave"


class GameEvent(StrEnum):
    """WebSocket message type"""

    ACTION_REQUEST = "ActionRequest"
    GAME_DATA = "GameData"
    ERROR = "Error"
    EVENT = "Event"
    GAME_FINISH = "GameFinish"
    INFO = "Info"
    NEW_STAGE = "NewStage"
    ROLE = "Role"
    GAME_START = "GameStart"


class LobbyAction(StrEnum):
    KICK = "Kick"
    START = "Start"
    DELETE = "Delete"
    LEAVE = "Leave"


class LobbyEvent(StrEnum):
    USER_CONNECT = "UserConnect"
    USER_LEAVE = "UserLeave"
    ERROR = "Error"


class PlayerStatusEnum(StrEnum):
    RAIDED = "Raided"  # by mafia
    ASSAULTED = "Assaulted"  # by maniac
    HEALED = "Healed"  # by doctor
    DISABLED = "Disabled"  # by prostitute

    HEALED_PREV = "HealedPrev"  # for doctor check
    DISABLED_PREV = "DisabledPrev"  # for prostitute check

    ACTED = "Acted"  # if role action performed

    UNTARGETABLE = "Untargetable"
