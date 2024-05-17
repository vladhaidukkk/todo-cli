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

# Dependencies Management
lock:
	uv pip compile pyproject.toml -o requirements.txt
	uv pip compile pyproject.toml --extra dev -o requirements-dev.txt

sync:
	uv pip sync requirements.txt

sync-dev:
	uv pip sync requirements-dev.txt

# Code Formatting & Linting
fmt:
	-isort todo
	-black todo
	-docformatter todo

lint:
	-pyright todo
	-flake8 todo
	-autoflake todo
	-bandit -c pyproject.toml -q -r todo
