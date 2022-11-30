from os import getcwd
from os.path import join
from pydantic import BaseSettings


class SettingsMixin(BaseSettings):
    class Config:
        env_file = join(getcwd(), ".env")
        env_file_encoding = "utf-8"


class Environment(SettingsMixin):
    """Environment configuration values for this app."""

    API_VERSION: str


class JWTEnvironment(SettingsMixin):
    # JWT Variables
    ALGORITHM: str = "HS256"
    SECRET_SECONDS: int = 300
    REFRESH_SECONDS: int = 18000
    SECRET: str
    REFRESH_KEY: str

    class Config:
        env_prefix = "JWT_"


class DatabaseEnvironment(SettingsMixin):
    """Database environment configuration values"""

    # DB Configuration variables
    DRIVER: str
    HOST: str
    PORT: str
    USER: str
    PWD: str
    NAME: str

    class Config:
        env_prefix = "DATABASE_"


environment = Environment()
database = DatabaseEnvironment()
jwt_environment = JWTEnvironment()
