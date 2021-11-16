from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserBase(BaseModel):
    phone: str
    name: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    age: Optional[int] = None
    date_of_birth: Optional[date] = None
    description: Optional[str] = None
    city: Optional[int] = None
    zodiac_sign: Optional[int] = None
    number: Optional[int] = None
    socionic_type: Optional[int] = None
    sixteen_pers_type: Optional[int] = None
    

class UserUpdate(UserBase):
    phone: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str]
    age: Optional[int] = None
    date_of_birth: Optional[date] = None
    description: Optional[str] = None
    city: Optional[int] = None
    zodiac_sign: Optional[int] = None
    number: Optional[int] = None
    socionic_type: Optional[int] = None
    sixteen_pers_type: Optional[int] = None
