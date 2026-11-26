from uuid import UUID

from presentation.http.base_dto import BaseDTO


class UserResponse(BaseDTO):
    id: UUID
    name: str
    email: str
