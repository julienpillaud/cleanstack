default:
    just --list

lint:
    uv run pre-commit run --all-files

tests *options="--log-cli-level=INFO":
    uv run pytest {{options}}
