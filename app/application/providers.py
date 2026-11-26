from dishka import Scope, Provider, AsyncContainer, provide

from domain.services import RoleDistributionService
from application.services import (
    JWTService,
    GameService,
    UserService,
    LobbyService,
    AvatarService,
    SecurityService,
    GameManagerService,
    RoomWebSocketService,
)
from infrastructure.websocket import WebSocketManager
from application.ws_message_handlers import (
    LobbyMessageHandler,
    GameWSMessageHandler,
)
from infrastructure.redis.repositories import GameRepository, LobbyRepository
from infrastructure.database.repositories import (
    UserRepository,
    AvatarRepository,
)


class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def jwt_service(self) -> JWTService:
        return JWTService()

    @provide(scope=Scope.REQUEST)
    def avatar_service(self, avatar_repo: AvatarRepository) -> AvatarService:
        return AvatarService(avatar_repo)

    @provide(scope=Scope.REQUEST)
    def game_service(
        self,
        game_repo: GameRepository,
        lobby_repo: LobbyRepository,
        role_distribution: RoleDistributionService,
    ) -> GameService:
        return GameService(game_repo, lobby_repo, role_distribution)

    @provide(scope=Scope.APP)
    def game_manager(
        self,
        container: AsyncContainer,
        websocket_manager: WebSocketManager,
    ) -> GameManagerService:
        return GameManagerService(container, websocket_manager)

    @provide(scope=Scope.REQUEST)
    def lobby_service(self, lobby_repo: LobbyRepository) -> LobbyService:
        return LobbyService(lobby_repo)

    @provide(scope=Scope.REQUEST)
    def user_service(
        self,
        user_repo: UserRepository,
        lobby_repo: LobbyRepository,
        game_repo: GameRepository,
        avatar_service: AvatarService,
    ) -> UserService:
        return UserService(user_repo, lobby_repo, game_repo, avatar_service)

    @provide(scope=Scope.REQUEST)
    def security_service(
        self, jwt_service: JWTService, user_repo: UserRepository
    ) -> SecurityService:
        return SecurityService(jwt_service, user_repo)

    @provide(scope=Scope.REQUEST)
    def game_ws_handler(
        self,
        game_service: GameService,
        game_manager: GameManagerService,
        websocket_manager: WebSocketManager,
    ) -> GameWSMessageHandler:
        return GameWSMessageHandler(
            game_service, game_manager, websocket_manager
        )

    @provide(scope=Scope.REQUEST)
    def lobby_ws_handler(
        self,
        game_service: GameService,
        lobby_service: LobbyService,
        lobby_repository: LobbyRepository,
        game_manager: GameManagerService,
        websocket_manager: WebSocketManager,
    ) -> LobbyMessageHandler:
        return LobbyMessageHandler(
            game_service,
            lobby_service,
            lobby_repository,
            game_manager,
            websocket_manager,
            websocket_manager,
        )

    @provide(scope=Scope.REQUEST)
    def room_ws_service(
        self,
        websocket_manager: WebSocketManager,
        game_ws_handler: GameWSMessageHandler,
        lobby_ws_handler: LobbyMessageHandler,
        user_service: UserService,
        lobby_service: LobbyService,
    ) -> RoomWebSocketService:
        return RoomWebSocketService(
            websocket_manager,
            game_ws_handler,
            lobby_ws_handler,
            user_service,
            lobby_service,
        )
