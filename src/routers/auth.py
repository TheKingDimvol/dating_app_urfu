from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from starlette import status

from src.controllers.auth import AuthController
from src.controllers.users import UserController
from src.schemas.auth import UserCredentials, TokenData


router = APIRouter(prefix='/auth', tags=['Authorization'])


@router.post("/login", response_model=TokenData)
async def login(user_data: UserCredentials):
    return await AuthController.login(user_data)


@router.post("/signup", response_model=TokenData)
async def signup(user_data: UserCredentials):
    return await AuthController.signup(user_data)


@router.post(
    "/test-method",
    description="Тестовый метод, чтобы посомтреть что лежит в токене"
)
async def method(token: TokenData):
    return AuthController.validate_token(token.access_token)


@router.post('/test_auth')
async def get_current_user(
    token: Optional[str] = Header(None)
):
    if not token:
        return {}
    curr_user = AuthController.validate_token(token)
    user_data = await UserController.get_by_id(curr_user['id'])
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_data
