from presentation.http.v1.responses.user_response import UserResponse


class PlayerResponse(UserResponse):
    is_alive: bool
