import os
import sys
import tomllib
from functools import cached_property
from pathlib import Path

from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseModel):
    pass


class Settings(BaseSettings):
    cli_name: str = "todo"
    is_win: bool = sys.platform.startswith("win")

    @computed_field
    @cached_property
    def data_dir(self) -> Path:
        data_home = (
            os.environ.get("LOCALAPPDATA", "~")
            if self.is_win
            else os.environ.get("XDG_DATA_HOME", "~/.local/share")
        )
        return Path(f"{data_home}/{self.cli_name}").expanduser()

    @computed_field
    @property
    def db_file(self) -> Path:
        return self.data_dir / f"{self.cli_name}.db"

    @computed_field
    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_file}"

    @computed_field
    @cached_property
    def config_dir(self) -> Path:
        config_home = (
            os.environ.get("LOCALAPPDATA", "~")
            if self.is_win
            else os.environ.get("XDG_CONFIG_HOME", "~/.config")
        )
        return Path(f"{config_home}/{self.cli_name}").expanduser()

    @computed_field
    @property
    def config_file(self) -> Path:
        return self.config_dir / f"{self.cli_name}.toml"

    @computed_field
    @cached_property
    def config(self) -> Config:
        if self.config_file.exists():
            with self.config_file.open("rb") as f:
                # TODO: parse user configurations & pass them to the Config
                contents = tomllib.load(f)  # noqa
        return Config()

    model_config = SettingsConfigDict(frozen=True)


settings = Settings()
