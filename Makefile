default: fmt

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
	-isort app
	-black app
	-docformatter app
