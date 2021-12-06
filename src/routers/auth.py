from fastapi import APIRouter

from controllers.auth import AuthController
from schemas.auth import UserCredentials, TokenData


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
