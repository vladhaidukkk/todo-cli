import os
import sys
import tomllib
from functools import cached_property
from pathlib import Path
from typing import Type

from pydantic import BaseModel, computed_field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class Config(BaseModel):
    pass


class Settings(BaseSettings):
    # Load from env variables.
    todo_config_posix: bool = False
    todo_config_roaming: bool = False

    # Constants (must be initialized to have the highest priority).
    cli_name: str
    is_win: bool

    @computed_field
    @cached_property
    def data_dir(self) -> Path:
        data_home = (
            os.environ.get(
                "APPDATA" if self.todo_config_roaming else "LOCALAPPDATA", "~"
            )
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
        if self.is_win:
            config_home = os.environ.get(
                "APPDATA" if self.todo_config_roaming else "LOCALAPPDATA", "~"
            )
            config_dir = self.cli_name
        else:
            config_home = (
                "~"
                if self.todo_config_posix
                else os.environ.get("XDG_CONFIG_HOME", "~/.config")
            )
            config_dir = (
                f".{self.cli_name}" if self.todo_config_posix else self.cli_name
            )
        return Path(f"{config_home}/{config_dir}").expanduser()

    @computed_field
    @property
    def config_file(self) -> Path:
        return self.config_dir / f"{self.cli_name}.toml"

    @computed_field
    @cached_property
    def config(self) -> Config:
        if self.config_file.exists():
            with self.config_file.open("rb") as f:
                # TODO: parse user configurations & pass them to the Config.
                contents = tomllib.load(f)  # noqa
        return Config()

    model_config = SettingsConfigDict(frozen=True)


settings = Settings(
    cli_name="todo",
    is_win=sys.platform.startswith("win"),
)


# Designed only for development. It prioritizes settings from a dotenv file, avoiding
# potential conflicts with env variables or secrets for real users.
class DotenvSettings(BaseSettings):
    debug: bool = False

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (dotenv_settings,)

    model_config = SettingsConfigDict(env_file=".env", frozen=True)


dev_settings = DotenvSettings()
