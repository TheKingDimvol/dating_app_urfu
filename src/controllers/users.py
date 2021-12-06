from db.users import users
from controllers.base import BaseController


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
            return {'Success': False, 'Error': str(error)}

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
            return {'Success': False, 'Error': str(error)}

    @classmethod
    async def update(cls, user_id, new_values):
        query = users.update() \
            .where(users.c.id == user_id).values(**new_values)
        res = await cls.db.execute(query)
        return res
