from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel


class PairCreate(BaseModel):
    first_user: int
    second_user: int
    like: Optional[Union[bool, None]] = None
    determined_date: Optional[Union[date, None]] = None


class Pair(PairCreate):
    id: int


class PairUpdate(BaseModel):
    like: Union[bool, None] = None
    determined_date: Union[date, None] = date.today()


class MsgCreate(BaseModel):
    text: str
    pair: int
    author: int
    is_read: Optional[bool] = False
    send_time: Optional[datetime] = None


class MsgUpdate(BaseModel):
    text: str
