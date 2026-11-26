from presentation.http.base_dto import BaseDTO


class LobbyLeaveResponse(BaseDTO):
    status: str
    message: str
    lobby_id: str
