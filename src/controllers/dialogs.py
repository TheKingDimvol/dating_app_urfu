from datetime import datetime

from sqlalchemy import and_

from src.db.messages import messages
from src.controllers.base import BaseController
from src.schemas.pairs import MsgCreate, MsgUpdate


class DialogController(BaseController):
    """Класс для операций, связанных с таблицей users
    """
    @classmethod
    async def get_user_dialogs(cls, curr_user):
        query = '''
        SELECT DISTINCT ON (pr.id) pair, text, author, ms.id, send_time, is_read
        FROM pairs pr
        JOIN messages ms ON ms.pair = pr.id
        WHERE (
            pr.first_user = :user_id 
            OR pr.second_user = :user_id
            )
            AND pr.like IS True
        ORDER BY pr.id, send_time desc 
        '''
        return await cls.db.fetch_all(query, {'user_id': curr_user['id']})

    @classmethod
    async def messages_read(cls, pair_id: int, author: int):
        query = messages.update().where(
            and_(messages.c.pair == pair_id, messages.c.author == author)
        ).values(is_read=True)
        return await cls.db.execute(query)

    @classmethod
    async def create_msg(cls, msg_obj: MsgCreate):
        query = messages.insert().values(
            text=msg_obj.text,
            pair=msg_obj.pair,
            author=msg_obj.author,
            is_read=False,
            send_time=datetime.utcnow()
        )
        return await cls.db.execute(query)

    @classmethod
    async def update_msg(cls, msg_id, msg_obj: MsgUpdate):
        query = messages.update().where(
            messages.c.id == msg_id
        ).values(text=msg_obj.text)
        return await cls.db.execute(query)
