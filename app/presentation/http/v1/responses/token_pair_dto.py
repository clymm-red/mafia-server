from presentation.http.base_dto import BaseDTO


class TokenPair(BaseDTO):
    access_token: str
    refresh_token: str
