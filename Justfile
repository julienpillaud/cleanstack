default:
    just --list

lint:
    uv run ruff check --fix || true
    uv run ruff format
    uv run ty check

tests *options="":
    uv run pytest {{ options }}

protests *options="":
    uv run protest run protests.session:session {{ options }}

dev:
    docker compose up -d

dev-down:
    docker compose down
