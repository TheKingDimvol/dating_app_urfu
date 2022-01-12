from datetime import datetime, timedelta

import asyncpg
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.hash import bcrypt

from src.controllers.base import BaseController
from src.schemas.auth import TokenData
from src.controllers.users import UserController
from src.settings import settings


class AuthController(BaseController):
    """Класс для операций, связанных с авторизацией
    """

    @classmethod
    async def login(cls, credentials):
        user = await UserController.get_by_phone(credentials.phone)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User doesn't exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not cls.verify_password(credentials.password, user.get('password')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong password!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = cls.create_token({
            'id': user.get('id'),
            'phone': user.get('phone')
        })

        fields = dict(**user)
        fields.pop('password')
        return {**token.dict(), **fields}

    @classmethod
    async def signup(cls, user):
        user.password = cls.hash_password(user.password)

        try:
            user_id = await UserController.create(user)
        except asyncpg.exceptions.UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this phone already exists!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return cls.create_token({
            'id': user_id,
            'phone': user.phone
        })

    @staticmethod
    def verify_password(plain_password: str, hashed_password) -> bool:
        try:
            return bcrypt.verify(plain_password, hashed_password)
        except ValueError:
            return False

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
