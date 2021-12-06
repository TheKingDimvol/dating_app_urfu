from pydantic import BaseModel
from typing import Optional
from datetime import date


class BaseUser(BaseModel):
    phone: str
    name: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class UserOut(BaseUser):
    id: int
    age: Optional[int] = None
    date_of_birth: Optional[date] = None
    description: Optional[str] = None
    city: Optional[int] = None
    zodiac_sign: Optional[int] = None
    number: Optional[int] = None
    socionic_type: Optional[int] = None
    sixteen_pers_type: Optional[int] = None
    

class UserUpdate(BaseUser):
    phone: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    age: Optional[int] = None
    date_of_birth: Optional[date] = None
    description: Optional[str] = None
    city: Optional[int] = None
    zodiac_sign: Optional[int] = None
    number: Optional[int] = None
    socionic_type: Optional[int] = None
    sixteen_pers_type: Optional[int] = None
