from fastapi import APIRouter, Depends

from src.controllers.profile import ProfileController
from src.middlewares.auth import get_current_user


router = APIRouter(prefix='/profile', tags=['Profile'])


@router.put("/")
async def get_users(update_params: dict, curr_user: dict = Depends(get_current_user)):
    return await ProfileController.update(curr_user['id'], update_params)
