from domain.enums import Topic, WebSocketMessageTypeEnum

from .lobby import WSLobbyDataPayload, LobbyCommandPayload
from .base_message import BaseMessage
from .game.responses.ws_game_data_payload import WSGameDataPayload
from .game.responses.ws_game_info_payload import WSGameInfoPayload
from .game.responses.ws_game_role_payload import WSGameRolePayload
from .game.requests.ws_game_command_payload import WSGameCommandPayload
from .game.responses.ws_game_new_stage_payload import WSGameNewStagePayload
from .game.responses.ws_game_action_request_payload import (
    WSGameActionRequestPayload,
)
from .game.responses.ws_user_connection_message_payload import (
    WSUserConnectionMessagePayload,
)


class WebSocketMessage(BaseMessage):
    """
    message_type (MessageTypeEnum)
    # topic (MessageTopicEnum)
    timestamp
    payload: {
        "action_type": "role_action" | "vote",
        "actor_role": RoleEnum
        "target": "<player_user_id>"
        "room_id": "<room_id>
    }
    """

    message_type: WebSocketMessageTypeEnum
    topic: Topic
    payload: (
        WSGameCommandPayload  # COMAND
        | WSGameInfoPayload  # INFO | ERROR
        | WSGameActionRequestPayload  # ACTION_REQUEST
        | WSGameNewStagePayload  # NEW_STAGE
        | WSGameDataPayload  # GAME_DATA
        | WSLobbyDataPayload  # LOBBY_DATA
        | LobbyCommandPayload  # COMAND
        | WSUserConnectionMessagePayload  # USER_CONNECT | USER_CONNECT
        | WSGameRolePayload
    )
