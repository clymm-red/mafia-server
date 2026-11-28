.SILENT:
.PHONY: dev lint fmt typecheck fix test

all: typecheck lint fmt

dev:
	-uv run uvicorn main:app --app-dir app --reload

lint:
	-uv run ruff check .

fmt:
	-uv run ruff format .

typecheck:
	-uv run ty check

fix:
	-uv run ruff check --fix .
	-uv run ruff format .

test:
	-uv run pytest
