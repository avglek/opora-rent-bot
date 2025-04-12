from dataclasses import dataclass
from dotenv import load_dotenv
from .base import getenv, ImproperlyConfigured


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class DataBaseConfig:
    database: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных

@dataclass
class Config:
    tg_bot: TelegramBotConfig
    db:DataBaseConfig


def load_config() -> Config:
    # Parse a `.env` file and load the variables into environment valriables
    load_dotenv()

    return Config(
        tg_bot=TelegramBotConfig(token=getenv("BOT_TOKEN")),
        db=DataBaseConfig(
            database=getenv('DATABASE'),
            db_host=getenv('DB_HOST'),
            db_user=getenv('DB_USER'),
            db_password=getenv('DB_PASSWORD')
        )
    )