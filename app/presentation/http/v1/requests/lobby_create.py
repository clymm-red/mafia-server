from presentation.http.base_dto import BaseDTO


class LobbyCreate(BaseDTO):
    max_players: int
