from fastapi import APIRouter
from typing import List

from src.schemas.users import UserCreate, UserOut, UserUpdate
from src.controllers.users import UserController


router = APIRouter(prefix='/users', tags=['UserTable'])


@router.get("/", response_model=List[UserOut])
async def get_users(limit: int = 100, skip: int = 0):
    return await UserController.get_all(limit, skip)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    return await UserController.get_by_id(user_id)


@router.post("/")
async def create_user(user: UserCreate):
    return await UserController.create(user)


@router.put(
    "/{user_id}",
    description="""
    Передать в Body параметры вида: 
    {
        "НазваниеСтолбца1": НовоеЗначение,
        "НазваниеСтолбца2": НовоеЗначение,
        ...
    }
    """
)
async def update_user(user_id: int, new_values: UserUpdate):
    return await UserController.update(user_id, new_values)


@router.delete("/all")
async def delete_all_users(password: str = None):
    return await UserController.delete_all(password)


@router.delete("/{user_id}", response_model=int)
async def delete_user(user_id: int):
    return await UserController.delete(user_id)
