"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""
import pathlib
import typing
import urllib.parse
from functools import lru_cache

from dotenv import find_dotenv
from pydantic import PostgresDsn, root_validator, validator
from pydantic.env_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr

from app.pkg.models.core.logger import LoggerLevel

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    """Base settings for all settings.

    Use double underscore for nested env variables.

    Examples:
    #    `.env` file should look like::
    #
    #       TELEGRAM__TOKEN=...
    #        TELEGRAM__WEBHOOK_DOMAIN_URL=...
    #
    #        LOGGER__PATH_TO_LOG="./src/logs"
    #        LOGGER__LEVEL="DEBUG"
    #
    #        API_SERVER__HOST="127.0.0.1"
    #        API_SERVER__PORT=9191

    Warnings:
        In the case where a value is specified for the same Settings field in multiple
        ways, the selected value is determined as follows
        (in descending order of priority):

        1. Arguments passed to the Settings class initializer.
        2. Environment variables, e.g., my_prefix_special_function as described above.
        3. Variables loaded from a dotenv (.env) file.
        4. Variables loaded from the secrets directory.
        5. The default field values for the Settings model.

    See Also:
        https://docs.pydantic.dev/latest/usage/pydantic_settings/
    """

    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True
        #: bool: case-sensitive for env variables.
        case_sensitive = True
        #: str: delimiter for nested env variables.
        env_nested_delimiter = "__"


class Postgresql(_Settings):
    """Postgresql settings."""

    #: str: Postgresql host.
    HOST: str #= "127.0.0.1"
    #HOST: str = "templatealanlatte-postgres-1"
    #: PositiveInt: positive int (x > 0) port of postgresql.
    PORT: PositiveInt #= 5432
    #: str: Postgresql user.
    USER: str #= "postgres"
    #: SecretStr: Postgresql password.
    PASSWORD: SecretStr #= SecretStr("123456")
    #: str: Postgresql database name.
    DATABASE_NAME: str #= "database1"

    #: PositiveInt: Min count of connections in one pool to postgresql.
    MIN_CONNECTION: PositiveInt = 1
    #: PositiveInt: Max count of connections in one pool  to postgresql.
    MAX_CONNECTION: PositiveInt = 16

    # str: Concatenation all settings for postgresql in one string. (DSN)
    #  Builds in `root_validator` method.
    DSN: typing.Optional[str] = None

    @root_validator(pre=True)
    def build_dsn(cls, values: dict):  # pylint: disable=no-self-argument
        """Build DSN for postgresql.

        Args:
            values: dict with all settings.

        Notes:
            This method is called before any other validation.
            I use it to build DSN for postgresql.

        See Also:
            About validators:
                https://pydantic-docs.helpmanual.io/usage/validators/#root-validators

            About DSN:
                https://pydantic-docs.helpmanual.io/usage/types/#postgresdsn

        Returns:
            dict with all settings and DSN.
        """

        values["DSN"] = PostgresDsn.build(
            scheme="postgresql",
            user=f"{values.get('USER')}",
            password=f"{urllib.parse.quote_plus(values.get('PASSWORD'))}",
            host=f"{values.get('HOST')}",
            port=f"{values.get('PORT')}",
            path=f"/{values.get('DATABASE_NAME')}",
        )
        return values


class Logging(_Settings):
    """Logging settings."""

    #: StrictStr: Level of logging which outs in std
    LEVEL: LoggerLevel = LoggerLevel.DEBUG
    #: pathlib.Path: Path of saving logs on local storage.
    FOLDER_PATH: pathlib.Path = pathlib.Path("./src/logs")

    @validator("FOLDER_PATH")
    def __create_dir_if_not_exist(  # pylint: disable=unused-private-member, no-self-argument
        cls,
        v: pathlib.Path,
    ):
        """Create directory if not exist."""

        if not v.exists():
            v.mkdir(exist_ok=True, parents=True)
        return v


class APIServer(_Settings):
    """API settings."""

    # --- API SETTINGS ---
    #: str: Name of API service
    INSTANCE_APP_NAME: str = "project_name"
    #: str: API host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of API.
    PORT: PositiveInt = 5000

    # --- SECURITY SETTINGS ---
    #: SecretStr: Secret key for token auth.
    #X_ACCESS_TOKEN: SecretStr = SecretStr("secret")
    #X_ACCESS_TOKEN: SecretStr = SecretStr("")
    X_ACCESS_TOKEN: SecretStr

    # --- OTHER SETTINGS ---
    #: Logging: Logging settings.
    LOGGER: Logging


class Centrifugo(_Settings):
    """Centrifugo settings."""

    #: str: Centrifugo host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of centrifugo.
    PORT: PositiveInt = 8001


class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev` if server running with parameter
    `dev`.
    """

    #  APIServer: API settings. Contains all settings for API.
    API: APIServer

    #: Postgresql: Postgresql settings.
    POSTGRES: Postgresql


# TODO: Возможно даже lru_cache не стоит использовать. Стоит использовать meta sigleton.
#   Для класса настроек. А инициализацию перенести в `def __init__`
@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""

    return Settings(_env_file=find_dotenv(env_file))
