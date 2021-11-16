from fastapi import APIRouter
from typing import List

from schemas.users import UserCreate, UserOut, UserUpdate
from controllers.users import UserController


router = APIRouter()


@router.get("/users/", response_model=List[UserOut])
async def get_users(limit: int = 100, skip: int = 0):
    return await UserController.get_all(limit, skip)


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    return await UserController.get_by_id(user_id)


@router.post("/users/")
async def create_user(user: UserCreate):
    return await UserController.create(user)

@router.put("/users/", description=
    """
    Передать в Body параметры вида: 
    {
        "НазваниеСтолбца1": НовоеЗначение,
        "НазваниеСтолбца2": НовоеЗначение,
        ...
    }
    """
)
async def update_user(user_id: int, new_values: dict):
    return await UserController.update(user_id, new_values)


@router.delete("/users/all")
async def delete_all_users(password: str = None):
    return await UserController.delete_all(password)


@router.delete("/users/{user_id}", response_model=int)
async def delete_user(user_id: int):
    return await UserController.delete(user_id)
