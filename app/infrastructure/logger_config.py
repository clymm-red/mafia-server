import sys
import json
import logging
from typing import Literal
from datetime import UTC, datetime


_HANDLER_NAME = "mafia-json-log"

_RESERVED_ATTRS = frozenset(
    {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "taskName",
        "thread",
        "threadName",
    }
)

_RESET = "\033[0m"
_KEY_COLOR = "\033[36m"  # cyan
_MESSAGE_COLOR = "\033[32m"  # green

_LEVEL_COLORS = {
    "DEBUG": "\033[36m",  # cyan
    "INFO": "\033[32m",  # green
    "WARNING": "\033[33m",  # yellow
    "ERROR": "\033[31m",  # red
    "CRITICAL": "\033[31m\033[47m",  # red on white
}


class JsonFormatter(logging.Formatter):
    def __init__(self, color: bool = False) -> None:
        super().__init__()
        self._color = color

    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "timestamp": datetime.fromtimestamp(
                record.created, UTC
            ).isoformat(),
        }

        # Поля, переданные через logger.info(..., extra={...})
        payload.update(
            {
                key: value
                for key, value in record.__dict__.items()
                if key not in _RESERVED_ATTRS and not key.startswith("_")
            }
        )

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack"] = record.stack_info

        if self._color:
            return self._colorize(payload, record.levelname)
        return json.dumps(payload, ensure_ascii=False, default=str)

    def _colorize(self, payload: dict, level: str) -> str:
        items = []
        for key, value in payload.items():
            rendered = json.dumps(value, ensure_ascii=False, default=str)

            if key == "level":
                color = _LEVEL_COLORS.get(level, "")
            elif key == "message":
                color = _MESSAGE_COLOR
            else:
                color = ""

            colored = f"{color}{rendered}{_RESET}" if color else rendered
            colored_key = (
                f"{_KEY_COLOR}{json.dumps(key, ensure_ascii=False)}{_RESET}"
            )
            items.append(f"{colored_key}: {colored}")

        return "{" + ", ".join(items) + "}"


def _supports_color() -> bool:
    stream = sys.stderr
    supports = getattr(stream, "isatty", None)
    return bool(stream is not None and supports is not None and stream.isatty())


def _configure_logging() -> None:
    root = logging.getLogger()
    if any(
        getattr(handler, "name", None) == _HANDLER_NAME
        for handler in root.handlers
    ):
        return

    handler = logging.StreamHandler()
    handler.name = _HANDLER_NAME
    handler.setFormatter(JsonFormatter(color=_supports_color()))
    root.addHandler(handler)


_configure_logging()


def get_logger(
    name: str,
    level: Literal[10, 20, 30, 40, 50] = 20,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
