from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
from middlewares.jwt_bearer import JWTBearer

user_router = APIRouter()

class User(BaseModel):
    email: str
    password: str

@user_router.post('/login', tags=['Auth'], status_code=200)
def login(user: User):
    if user.email == JWTBearer.email and user.password == JWTBearer.password:
        token:str = create_token(user.dict())
    return JSONResponse(content=token, status_code=200)