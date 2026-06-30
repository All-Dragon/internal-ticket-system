import os
from dataclasses import dataclass

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
    url: str


@dataclass
class AdminCredentials:
    username: str
    password: str


@dataclass
class Config:
    db: DatabaseSettings
    api: APISettings
    jwt: JWTSettings
    adminCred: AdminCredentials


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    db = DatabaseSettings(
        url=env("DATABASE_URL", "sqlite+aiosqlite:///./app.db"),
    )

    api = APISettings(
        base_url=os.getenv("API_BASE_URL", "http://localhost:8000"),
    )

    jwt = JWTSettings(
        SECRET_KEY=os.getenv("SECRET_KEY", "change-me-in-real-projects"),
        ALGORITHM=os.getenv("ALGORITHM", "HS256"),
        ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
    )

    admin_cred = AdminCredentials(
        username=env("ADMIN_USERNAME"),
        password=env("ADMIN_PASSWORD"),
    )

    return Config(db=db, api=api, jwt=jwt, adminCred=admin_cred)


def generate_url_db():
    config: Config = load_config()
    return config.db.url
