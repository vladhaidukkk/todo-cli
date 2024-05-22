import os
import sys
from functools import cached_property
from pathlib import Path


class Config:
    cli_name: str = "todo"

    @cached_property
    def data_dir(self) -> Path:
        is_win = sys.platform.startswith("win")
        data_home = (
            os.environ.get("LOCALAPPDATA", "~")
            if is_win
            else os.environ.get("XDG_DATA_HOME", "~/.local/share")
        )
        return Path(f"{data_home}/{self.cli_name}").expanduser()

    @cached_property
    def db_file(self) -> Path:
        return self.data_dir / f"{self.cli_name}.db"

    @cached_property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_file}"


config = Config()
