from .config import config
from .main import app

app(prog_name=config.cli_name)
