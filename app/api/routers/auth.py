from fastapi import APIRouter

from app.schemas import AdminLogin, Token
from app.services import AuthService

authorization_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@authorization_router.post("/login", response_model=Token)
async def login_admin(data: AdminLogin):
    return await AuthService.login_admin(data=data)