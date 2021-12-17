from fastapi import APIRouter
from typing import List

from src.schemas.users import UserOut
from src.controllers.users import UserController
from src.controllers.pairs import PairController


router = APIRouter(prefix='/pairs', tags=['PairTable'])

@router.get("/list_for_swipe")
async def get_list_for_swipe(user_id: int):
    return await PairController.get_list_for_swipe(user_id)


