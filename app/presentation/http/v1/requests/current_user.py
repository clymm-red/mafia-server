from uuid import UUID

from presentation.http.base_dto import BaseDTO


class CurrentUser(BaseDTO):
    id: UUID
    username: str
    email: str
