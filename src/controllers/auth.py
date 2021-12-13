from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError

from src.controllers.base import BaseController
from src.schemas.auth import TokenData, UserCredentials
from src.schemas.users import User
from src.controllers.users import UserController
from src.settings import settings


class AuthController(BaseController):
    """Класс для операций, связанных с авторизацией
    """

    @classmethod
    async def login(cls, credentials):
        user = await UserController.get_by_phone(credentials.phone)
        # TODO normal errors with codes
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User doesn't exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not cls.verify_password(credentials.password, user.get('password')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong password!!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return cls.create_token({
            'id': user.get('id'),
            'phone': user.get('phone')
        })

    @classmethod
    async def signup(cls, user):
        user.password = cls.hash_password(user.password)

        try:
            user_id = await UserController.create(user)
        except Exception as e:
            raise e

        return cls.create_token({
            'id': user_id,
            'phone': user.phone
        })

    @staticmethod
    def verify_password(plain_password: str, hashed_password) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def validate_token(token: str):
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload.get('user') or None

    @staticmethod
    def create_token(user: dict) -> TokenData:
        now = datetime.now()

        payload = {
            'iat': now,
            'nbf': 0,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user['id']),
            'user': user
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )

        return TokenData(access_token=token)
