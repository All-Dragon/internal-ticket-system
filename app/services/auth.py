import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.JWT.security import create_access_token
from app.core.JWT.token_shemas import Token, UserLogin
from app.core.hash import verify_password
from app.repositories import UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    async def login(data: UserLogin, session: AsyncSession) -> Token:
        logger.info("Token request for user %s", data.email)

        user = await UserRepository.get_by_email(
            email=data.email,
            session=session,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
            )

        try:
            access_token = create_access_token(
                data={"email": user.email, "role": user.role}
            )
        except Exception:
            logger.exception("Token generation error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token generation error",
            )

        return Token(access_token=access_token, token_type="bearer")
