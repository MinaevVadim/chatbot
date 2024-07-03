import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = f"{pathlib.Path(__file__).resolve().parent.parent}/.env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=env_file,
    )
    secret_key: str
    bot_token: str
    db_name: str = "admin"
    db_user: str = "admin"
    db_pass: str = "admin"


settings = Settings()
