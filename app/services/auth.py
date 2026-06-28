import logging
from datetime import timedelta

from fastapi import HTTPException, status

from app.core.JWT.security import create_access_token
from app.core.config_app import Config, load_config
from app.schemas import AdminLogin, Token

logger = logging.getLogger(__name__)
config: Config = load_config()

class AuthService:
    @staticmethod
    async def login_admin(data: AdminLogin) -> Token:
        logger.info("Попытка входа администратора username=%s", data.username)

        if data.username != "admin" or data.password != "admin":
            logger.warning("Неуспешная попытка входа администратора username=%s", data.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверные учетные данные администратора",
            )

        access_token = create_access_token(
            data={"sub": data.username, "role": "admin"},
            expires_delta=timedelta(minutes=config.jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return Token(access_token=access_token)