from fastapi import HTTPException, status
from passlib.hash import bcrypt

from src.controllers.base import BaseController
from src.db.users import UPDATE_COLUMNS
from src.controllers.users import UserController


class ProfileController(BaseController):
    """Класс для операций, связанных с профилем пользователя
    """

    @classmethod
    async def update(cls, user_id: int, new_values: dict):
        if not new_values:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="No new data to modify!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if 'id' in new_values or 'phone' in new_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot update user's id or phone!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        for column, value in new_values.items():
            if column not in UPDATE_COLUMNS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Column '{column}' doesn't exist!",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if column == 'password':
                new_values[column] = cls.process_password(value)
            # todo ограничения на все другие поля! Узнать что нам будут передавать!

        return await UserController.update(user_id, new_values)

    @staticmethod
    def process_password(password: str) -> str:
        if not isinstance(password, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Column 'password' must be a string!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return bcrypt.hash(password)
