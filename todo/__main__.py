from todo.config import settings
from todo.main import app

app(prog_name=settings.cli_name)
