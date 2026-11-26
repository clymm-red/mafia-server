from presentation.http.base_dto import BaseDTO


class UserCreate(BaseDTO):
    username: str
    email: str
    password: str
