import os
from dataclasses import dataclass
from urllib.parse import quote

from environs import Env


@dataclass
class JWTSettings:
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


@dataclass
class APISettings:
    base_url: str


@dataclass
class DatabaseSettings:
    name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class RedisSettings:
    host: str
    port: int
    db: int
    password: str
    username: str


@dataclass
class Config:
    db: DatabaseSettings
    redis: RedisSettings
    api: APISettings
    jwt: JWTSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    db = DatabaseSettings(
        name=env("DB_NAME", "starterkit"),
        host=env("DB_HOST", "localhost"),
        port=env.int("DB_PORT", 5432),
        user=env("DB_USER", "starterkit"),
        password=env("DB_PASSWORD", "starterkit"),
    )

    redis = RedisSettings(
        host=env("REDIS_HOST", "localhost"),
        port=env.int("REDIS_PORT", 6379),
        db=env.int("REDIS_DATABASE", 0),
        password=env("REDIS_PASSWORD", default=""),
        username=env("REDIS_USERNAME", default=""),
    )

    api = APISettings(
        base_url=os.getenv("API_BASE_URL", "http://localhost:8000"),
    )

    jwt = JWTSettings(
        SECRET_KEY=os.getenv("SECRET_KEY", "change-me-in-real-projects"),
        ALGORITHM=os.getenv("ALGORITHM", "HS256"),
        ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
    )

    return Config(db=db, redis=redis, api=api, jwt=jwt)


def generate_url_db():
    config: Config = load_config()
    url = (
        f"postgresql+asyncpg://{quote(config.db.user, safe='')}:"
        f"{quote(config.db.password, safe='')}@{config.db.host}:{config.db.port}/{config.db.name}"
    )
    return url
