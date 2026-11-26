from dishka import Scope, Provider, provide
from fastapi import Request

from application.services import SecurityService
from presentation.http.v1.requests import CurrentUser


class AuthProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_current_user(
        self, request: Request, security_service: SecurityService
    ) -> CurrentUser:
        token = request.headers.get("authorization", "").removeprefix("Bearer ")
        return await security_service.get_current_user(token)
