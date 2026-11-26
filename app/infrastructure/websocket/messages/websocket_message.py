from domain.enums import Topic, WebSocketMessageTypeEnum

from .base_websocket_message import BaseWebSocketMessage
from .responses.ws_game_data_payload import WSGameDataPayload
from .responses.ws_game_info_payload import WSGameInfoPayload
from .responses.ws_game_role_payload import WSGameRolePayload
from .responses.ws_lobby_data_payload import WSLobbyDataPayload
from .requests.ws_game_command_payload import WSGameCommandPayload
from .requests.ws_lobby_command_payload import LobbyCommandPayload
from .responses.ws_game_new_stage_payload import WSGameNewStagePayload
from .responses.ws_game_action_request_payload import WSGameActionRequestPayload
from .responses.ws_user_connection_message_payload import (
    WSUserConnectionMessagePayload,
)


class WebSocketMessage(BaseWebSocketMessage):
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
    timestamp: str
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
