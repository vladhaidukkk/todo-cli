default: fmt lint

# CLI Management
init:
	uv pip install .

init-dev:
	uv pip install -e .

gen-doc:
	typer todo.main utils docs --name todo --title "Usage Guide for Todo CLI" --output docs/USAGE_GUIDE.md

build:
	python -m build

publish-test:
    twine upload --verbose -r testpypi dist/*

# Dependencies Management
try pkg:
    uv pip install --dry-run {{pkg}}

rm pkg:
    uv pip uninstall {{pkg}}

lock:
	uv pip compile pyproject.toml -o requirements.txt
	uv pip compile pyproject.toml --extra dev -o requirements-dev.txt

lock-up:
	uv pip compile pyproject.toml --upgrade -o requirements.txt
	uv pip compile pyproject.toml --extra dev --upgrade -o requirements-dev.txt

sync:
	uv pip sync requirements.txt

sync-dev: && init-dev
	uv pip sync requirements-dev.txt

list:
    uv pip list

info pkg:
    uv pip show {{pkg}}

health:
    uv pip check

# Code Formatting & Linting
fmt:
	-ruff format todo tests

lint:
	-pyright todo tests
	-ruff check todo tests
	-bandit -c pyproject.toml -q -r todo

fix:
    -ruff check --fix todo tests

# Database Management
alembic := "alembic -c todo/db/alembic.ini"

revise msg:
    {{alembic}} revision --autogenerate -m "{{msg}}"

migrate target="head":
    {{alembic}} upgrade {{target}}

revert target="-1":
    {{alembic}} downgrade {{target}}
