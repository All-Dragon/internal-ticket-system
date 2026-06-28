from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.JWT.security import decode_token

bearer_scheme = HTTPBearer()

async def require_admin(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    payload = decode_token(credentials.credentials)

    if payload.get("sub") != "admin" or payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Требуются права администратора",
        )

    return payload