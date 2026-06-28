from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Token_Data(BaseModel):
    email: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str
