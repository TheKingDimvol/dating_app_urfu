from typing import Optional, List

from fastapi import APIRouter, Depends

from src.controllers.pairs import PairController
from src.middlewares.auth import get_current_user
from src.schemas.pairs import PairUpdate, PairCreate, Pair

router = APIRouter(prefix='/pairs', tags=['PairTable'])


@router.get("/list_for_swipe")
async def get_list_for_swipe(user_id: int):
    return await PairController.get_list_for_swipe(user_id)


@router.put("/like/{user_id}")
async def like(user_id: int, liked: bool, curr_user: dict = Depends(get_current_user)):
    return await PairController.like_user(user_id, curr_user, liked)


@router.get("/", tags=['MethodsForDirectAccess'], response_model=List[Pair])
async def get_pairs(
        id: Optional[int] = None,
        user: Optional[int] = None,
        second_user: Optional[int] = None
):
    if id:
        return await PairController.get_pairs(pair_id=id)
    if user and second_user:
        return await PairController.get_pairs(
            first_user=user, second_user=second_user
        )
    if user or second_user:
        return await PairController.get_pairs(
            first_user=user or second_user
        )
    return await PairController.get_pairs()


@router.post("/", tags=['MethodsForDirectAccess'])
async def create_pair(pair: PairCreate):
    return await PairController.create_pair(pair)


@router.put("/{pair_id}", tags=['MethodsForDirectAccess'])
async def update_pair(pair_id: int, pair: PairUpdate):
    return await PairController.update_pair(pair_id, pair)
