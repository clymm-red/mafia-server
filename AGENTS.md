# AGENTS.md

Guidance for AI coding agents working on the Mafia game backend.

## Project snapshot

- Backend for a social-deduction game (Mafia). The frontend lives in a
  separate repository: <https://github.com/decisivestrike/mafia-client>.
- Python 3.14, FastAPI, Dishka (DI), SQLAlchemy 2 async + asyncpg, Redis,
  S3-compatible storage (RustFS), JWT, WebSocket.
- `docs/API_CONTRACT.md` is the source of truth for the WebSocket contract.
- `bruno/` contains a manual HTTP collection used during development.

## Commands

```bash
uv sync                      # install dependencies
make dev                     # uv run uvicorn main:app --app-dir app --reload
make lint                    # uv run ruff check .
make fmt                     # uv run ruff format .
make typecheck               # uv run ty check
make fix                     # ruff check --fix + ruff format
make test                    # uv run pytest
make all                     # typecheck + lint + fmt (does NOT run tests)
```

Notes:

- Makefile targets start with `-`, so a failing step does not stop the run.
  Always inspect the output instead of trusting the exit code.
- Infrastructure: `docker compose --profile db up -d` starts Postgres, Redis
  and RustFS; `--profile all` starts the full stack including the backend.
- A `.env` file is required. Settings are declared in
  `app/infrastructure/environment.py` (`POSTGRES_*`, `REDIS_URL`, `JWT_*`,
  `RUSTFS_*`, `DEBUG`). Never commit `.env`.
- Tests need Postgres, Redis and RustFS running: the FastAPI lifespan creates
  the tables and ensures the S3 bucket. There is no Alembic; the schema is
  created by `create_tables()` on startup.

## Architecture: Clean Architecture + DDD

### Dependency rule

```text
presentation ──▶ application ──▶ domain
                     ▲
infrastructure ──────┘  (implements ports declared by inner layers)
```

- Inner layers must not import outer layers.
- `domain` must not know about FastAPI, Pydantic, SQLAlchemy, Redis, S3, HTTP
  or WebSocket.
- `application` coordinates use cases and depends only on the domain and on
  ports.
- `infrastructure` implements ports and knows about technologies.
- `presentation` translates external requests into use-case calls.
- `app/main.py` is the composition root: it builds the Dishka container,
  registers providers and routers, and maps exceptions to HTTP responses.

### Layers

| Layer              | Components                                                                                  | Responsibility                                              |
| ------------------ | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Domain**         | Entities, Value Objects, Domain Services, Domain Exceptions, Ports (Interfaces)             | Business rules and invariants; no technical details         |
| **Application**    | Use Cases, Application Services, Mappers                                                    | Scenario orchestration, transaction boundaries, DTO mapping |
| **Infrastructure** | Repository implementations, Redis/S3/JWT/WebSocket/logging adapters, DI providers           | Implement ports; integrate with external systems            |
| **Presentation**   | HTTP/WS controllers and routers, request/response DTOs, exception mapping, composition root | Delivery layer and input validation                         |

### DDD map

- Aggregates:
  - `Game` — aggregate root: players, stage, votes, winner and finish
    conditions.
  - `Lobby` — aggregate root: admin, participants, capacity.
  - `User` — aggregate root for identity and profile data.
- Entity inside an aggregate: `Player` (a user's in-game state and role).
- Domain objects: the `Role` hierarchy (`Citizen`, `Doctor`, `MafiaMember`,
  `MafiaDon`, `Sheriff`, `Prostitute`, `Maniac`).
- Domain services: `RoleDistributionService`, `VoteConductorService`.
- Value objects: enum values and identifiers are the current form; there are
  no dedicated VO classes yet.

### Ubiquitous language

| Term   | Meaning                                                       |
| ------ | ------------------------------------------------------------- |
| Lobby  | Pre-game room where players gather before the game starts     |
| Game   | A running match with a stage loop and win conditions          |
| Player | A user's participation in a game, including role and statuses |
| Role   | A game role with team and night action                        |
| Team   | `CitizenTeam`, `MafiaTeam`, `Neutral`                         |
| Stage  | `DayIntro`, `DayTalk`, `DayVote`, `Night`                     |
| Action | Client intent: `Vote`, `RoleAction`, `EndTalk`, `Leave`       |

### Ports

New repositories and external clients must be declared as an `ABC` with
`@abstractmethod` in `domain` and implemented in `infrastructure`. Application
services and use cases depend on the port, never on the concrete adapter.

```python
# domain/repositories/lobby_repository.py
from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.lobby import Lobby


class LobbyRepository(ABC):
    @abstractmethod
    async def get_by_id(self, lobby_id: str) -> Lobby | None: ...

    @abstractmethod
    async def add_participant(
        self, lobby_id: str, user_id: UUID
    ) -> Lobby: ...
```

```python
# infrastructure/redis/repositories/lobby_repository.py
class RedisLobbyRepository(LobbyRepository):
    ...
```

Do not migrate existing concrete repositories to ports unless the task asks
for it.

### DTOs and mappers

- DTOs live on the boundaries (`presentation`, and `application` when needed),
  never in `domain`.
- Domain entities must not leak outside; map them to DTOs in mappers or
  response factories.
- Pydantic models are boundary/persistence models, not domain models.

### Composition and DI

- Dishka providers are split by layer: `domain/providers.py`,
  `application/providers.py`, `infrastructure/providers.py`,
  `presentation/providers.py`.
- Use `@inject` on endpoints and `FromDishka[T]` for dependencies.
- `Scope.APP` — long-lived singletons (containers, managers, factories);
  `Scope.REQUEST` — services, repositories, sessions.
- Long-running game loops live in `GameManagerService` and use
  `RequestScopedProxy` to resolve request-scoped services per operation.
  They are in-memory and per-process, so the app is not horizontally
  scalable as-is.

### Current deviations (tech debt)

The code does not yet fully follow the dependency rule:

- `domain` imports `infrastructure.logger`.
- `application` imports concrete `infrastructure.repositories` and
  `presentation` DTOs.
- Repository ports do not exist yet.

Do not add new outward dependencies. When touching these files, prefer moving
toward ports, but do not perform opportunistic refactors without agreement.

## WebSocket protocol

- Endpoint: `/rooms/{room_id}`.
- Authentication: `Authorization: Bearer <token>` header, or the
  `authorization` query parameter as a fallback.
- Incoming envelope: `topic`, `action`, `timestamp`, `payload`.
- Outgoing envelope: `event`, `timestamp`, `payload`.
- `timestamp` is optional and defaults to the current time.
- JSON is camelCase (`alias_generator=to_camel`), unknown fields are forbidden
  on messages, and the envelope allows extra fields to carry the action
  payload.

Message classes live under
`app/infrastructure/websocket/messages/{lobby,game}/{incoming,outgoing}`.
Incoming messages are discriminated unions by `action`; outgoing messages are
created through `.create(...)` factories and sent via `WebSocketManager`.

Checklist for a new incoming message:

1. Add or reuse the action in `domain/enums.py`.
2. Add the payload and message classes.
3. Export them in the package `__init__.py` and update the adapter union.
4. Handle the payload in the matching `GameWSMessageHandler` or
   `LobbyMessageHandler`.
5. Update `docs/API_CONTRACT.md`.
6. Update the Bruno collection if an HTTP endpoint is involved.

Errors: a `DomainException` carrying a `Topic` is converted to the matching
`Error` event. HTTP exceptions are mapped in `app/main.py`. Enum values are
part of the wire contract; never rename them without updating the client and
`docs/API_CONTRACT.md`.

## Code conventions

- Use full type hints and modern syntax: `X | None`, `Self`, `match`,
  `assert_never`.
- Async everywhere: no blocking I/O; use `redis.asyncio` and async
  SQLAlchemy.
- Ruff: 80-character lines, double quotes, isort with `length-sort`; enabled
  rules are `I`, `F`, `FAST`, `E`, `W`, `PERF`, `UP`. Run `make fix` before
  finishing.
- `ty` is the type-checking gate (`make typecheck`). `pyrightconfig.json` is
  present but is not the CI gate.
- Pydantic v2: use `ConfigDict`, `Field(default_factory=...)` and
  `model_dump(by_alias=True)`.
- Exceptions follow `AppException → DomainException / RepoException /
  TokenException`. Raise domain exceptions for business-rule violations; do
  not swallow errors.
- Use `infrastructure.logger.get_logger`; do not add new `print` calls.
- Naming: modules and functions `snake_case`, classes `PascalCase`, enums
  `StrEnum` with `UPPER_CASE` members.
- Imports resolve from the `app` root (`pythonpath = ["app"]` in pytest). Use
  the existing barrel imports from package `__init__.py` files.
- User-facing messages and logs are in Russian; identifiers and docstrings
  follow the local file style.

## Rules for agents

- Never read, modify or commit `.env` or any secret. Never print tokens.
- Manage dependencies only with `uv add` / `uv remove`. Do not edit
  `uv.lock` by hand and do not use `pip`.
- Before finishing, run:
  `uv run ruff check .`, `uv run ruff format .`, `uv run ty check`,
  `uv run pytest` (or `make all` plus `make test`). Report failures honestly.
- Ask before changing the architecture, public HTTP/WS contracts, the database
  schema, dependencies, services or environment variables, and before large
  refactors.
- Do not disable linters or type checks, do not add unjustified
  `# type: ignore`, and do not weaken tests.
- Keep `docs/API_CONTRACT.md` in sync with the code.
- New code follows Clean Architecture + DDD: dependencies point inward, DTOs
  stay on the boundaries, and new adapters get a port.
