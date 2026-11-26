from presentation.http.base_dto import BaseDTO


class RoomResponse(BaseDTO):
    room_id: str
    is_lobby: bool
