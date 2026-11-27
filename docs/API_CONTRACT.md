Event - сообщение + отрисовка или изменение чего либо
Info - просто сообщение

## Веб-сокеты

Входящие сообщения (клиент → сервер) описываются парой **action + payload**.
Исходящие сообщения (сервер → клиент) описываются парой **event + payload**.

Общий вид входящего сообщения:

```json
{
  "topic": "Lobby" | "Game",
  "action": "<action>",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {}
}
```

Общий вид исходящего сообщения:

```json
{
  "event": "<event>",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {}
}
```

`timestamp` необязателен: если клиент его не передал, сервер подставит текущее время.

## То, что отправляет клиент серверу

### Лобби

Начать игру

```json
{
  "topic": "Lobby",
  "action": "Start",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "roomId": "room_id",
    "roleSet": ["MafiaMember", "Citizen", "Doctor"]
  }
}
```

Выпнуть участника

```json
{
  "topic": "Lobby",
  "action": "Kick",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "roomId": "room_id",
    "targetId": "target_id"
  }
}
```

Удалить лобби (хост)

```json
{
  "topic": "Lobby",
  "action": "Delete",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "roomId": "room_id"
  }
}
```

Выйти из лобби

```json
{
  "topic": "Lobby",
  "action": "Leave",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "roomId": "room_id"
  }
}
```

### Игра

Сделать ночной ход

```json
{
  "topic": "Game",
  "action": "RoleAction",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "roomId": "room_id",
    "targetId": "target_id"
  }
}
```

Пропустить речь

```json
{
  "topic": "Game",
  "action": "EndTalk",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "roomId": "room_id"
  }
}
```

Проголосовать

```json
{
  "topic": "Game",
  "action": "Vote",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "roomId": "room_id",
    "targetId": "target_id"
  }
}
```

Выйти из игры

```json
{
  "topic": "Game",
  "action": "Leave",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "roomId": "room_id"
  }
}
```

## То, что отправляет сервер клиенту

`actor_id` в исходящих сообщениях не передаётся: сервер берёт его из
аутентифицированного подключения.

### Лобби

Подключение пользователя

```json
{
  "event": "UserConnect",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "id": "user_id",
    "name": "username"
  }
}
```

Отключение пользователя

```json
{
  "event": "UserLeave",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "id": "user_id",
    "name": "username"
  }
}
```

Ошибка лобби

```json
{
  "event": "Error",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "text": "Текст ошибки"
  }
}
```

### Игра

Начало игры

```json
{
  "event": "GameStart",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "text": "Игра началась"
  }
}
```

Конец игры

```json
{
  "event": "GameFinish",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "text": "Игра окончилась победой MafiaTeam"
  }
}
```

Событие в игре (отрисовка или изменение)

```json
{
  "event": "Event",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "text": "Текст события"
  }
}
```

Информационное сообщение

```json
{
  "event": "Info",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "text": "Текст сообщения"
  }
}
```

Ошибка игры

```json
{
  "event": "Error",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "text": "Текст ошибки"
  }
}
```

Запрос действия у игрока

```json
{
  "event": "ActionRequest",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "text": "Выберите игрока",
    "timeout": 30
  }
}
```

Новая стадия игры

```json
{
  "event": "NewStage",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "newStage": "Night",
    "text": "Город засыпает"
  }
}
```

Роль игрока

```json
{
  "event": "Role",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "text": "Ваша роль",
    "role": "Sheriff"
  }
}
```

Состояние игры

```json
{
  "event": "GameData",
  "timestamp": "2026-03-18T14:18:57.306565",
  "payload": {
    "id": "game_id",
    "players": [
      {
        "id": "user_id",
        "name": "username",
        "email": "user@example.com",
        "isAlive": true
      }
    ],
    "admin": {
      "id": "admin_id",
      "name": "admin",
      "email": "admin@example.com",
      "isAlive": true
    },
    "startDate": "2026-03-18T14:18:57.306565",
    "assignedRole": "Citizen",
    "winnerTeam": null,
    "gameStatus": "In progress",
    "gameStage": "Night",
    "finishDate": null,
    "roundCount": 1
  }
}
```

## Значения enum'ов

- `Topic`: `Lobby`, `Game`
- `LobbyAction`: `Start`, `Kick`, `Delete`, `Leave`
- `GameAction`: `RoleAction`, `EndTalk`, `Vote`, `Leave`
- `LobbyEvent`: `UserConnect`, `UserLeave`, `Error`
- `GameEvent`: `GameStart`, `GameFinish`, `Event`, `Info`, `Error`, `ActionRequest`, `NewStage`, `Role`, `GameData`
- `GameStage`: `DayIntro`, `DayTalk`, `DayVote`, `Night`
- `GameStatusEnum`: `In progress`, `Paused`, `Finished`
- `TeamEnum`: `None`, `CitizenTeam`, `MafiaTeam`, `Neutral`
- `RoleEnum`: `Citizen`, `MafiaMember`, `Sheriff`, `Doctor`, `MafiaDon`, `Prostitute`, `Maniac`, `DeputySheriff`, `Shapeshifter`
