from fastapi import HTTPException, status

from src.db.users import users
from src.controllers.base import BaseController
from src.person_tests.personalities16_types import PersonalitiesTypes
from src.person_tests.socionic_types import SocionicTypes


class UserController(BaseController):
    """Класс для операций, связанных с таблицей users
    """
    @classmethod
    async def get_all(cls, limit, skip):
        query = users.select().limit(limit).offset(skip)
        return await cls.db.fetch_all(query)

    @classmethod
    async def get_by_phone(cls, phone):
        query = users.select().where(users.c.phone == phone)
        return await cls.db.fetch_one(query)

    @classmethod
    async def get_by_id(cls, user_id: int):
        query = users.select().where(users.c.id == user_id)
        return await cls.db.fetch_one(query)

    @classmethod
    async def create(cls, user):
        query = users.insert().values(**user.dict())
        user_id = await cls.db.execute(query)
        return user_id

    @classmethod
    async def delete(cls, user_id: int):
        try:
            query = users.delete().where(users.c.id == user_id)
            await cls.db.execute(query)
            return {'Success': True}
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Эта функция удаляет всех пользователей из таблицы, но нужен пароль
    # TODO В будующем убрать или добавить безопасность
    @classmethod
    async def delete_all(cls, password):
        if password != '123':
            return {'Error': 'No access!'}
        try:
            query = users.delete()
            await cls.db.execute(query)
            return {'Success': True}
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
                headers={"WWW-Authenticate": "Bearer"},
            )

    @classmethod
    async def update(cls, user_id, new_values: dict):
        query = users.update() \
            .where(users.c.id == user_id).values(new_values)
        res = await cls.db.execute(query)
        return res

    @classmethod
    async def update_socionic(cls, user_id, socionic_type):
        try:
            new_type = SocionicTypes[socionic_type.upper()].value
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error) + ", this type does not exist",
                headers={"WWW-Authenticate": "Bearer"},
            )
        query = """UPDATE users SET socionic_type = :type
            WHERE id = :user_id
            """
        res = await cls.db.execute(query=query, values={"user_id": user_id,
                                                            "type": new_type})
        return res

    @classmethod
    async def update_personalit(cls, user_id, personalit_type):
        try:
            new_type = PersonalitiesTypes[personalit_type.upper()].value
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error) + ", this type does not exist",
                headers={"WWW-Authenticate": "Bearer"},
            )
        query = """UPDATE users SET sixteen_pers_type = :type
                WHERE id = :user_id
                """
        res = await cls.db.execute(query=query, values={"user_id": user_id,
                                                        "type": new_type})
        return res


