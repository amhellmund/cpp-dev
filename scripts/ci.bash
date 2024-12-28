#! /bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR="${SCRIPT_DIR}/.."

echo "Running pytests"
uv run pytest ${ROOT_DIR}

echo "Running ruff check"
uv run ruff check

echo "Running mypy"
uv run mypy ${ROOT_DIR}