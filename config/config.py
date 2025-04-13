from dataclasses import dataclass
from dotenv import load_dotenv
from .base import getenv, ImproperlyConfigured


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class DataBaseConfig:
    database: str      # Название базы данных
    host: str          # URL-адрес базы данных
    user: str          # Username пользователя базы данных
    password: str      # Пароль к базе данных
    localdb:str        # Локальная база sqlite

    def get_url(self)->str:
        return f"postgresql://{self.user}:{self.password}@{self.host}/{self.database}"

    def get_local_url(self)->str:
        return f"sqlite:///{self.localdb}"

@dataclass
class Config:
    tg_bot: TelegramBotConfig
    db: DataBaseConfig


def load_config() -> Config:
    # Parse a `.env` file and load the variables into environment valriables
    load_dotenv()

    return Config(
        tg_bot=TelegramBotConfig(token=getenv("BOT_TOKEN")),
        db=DataBaseConfig(
            database=getenv('DATABASE'),
            host=getenv('DB_HOST'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASSWORD'),
            localdb=getenv('LOCAL_DB_PATH')
        )
    )