default:
    just --list

lint:
    uv run pre-commit run --all-files

tests *options="":
    uv run pytest {{ options }}

protests *options="":
    uv run protest run protests.session:session {{ options }}

dev:
    docker compose up -d

dev-down:
    docker compose down
