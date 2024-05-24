from .config import settings
from .main import app

app(prog_name=settings.cli_name)
