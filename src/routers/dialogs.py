from fastapi import APIRouter, Depends
from typing import List

from src.controllers.dialogs import DialogController
from src.middlewares.auth import get_current_user
from src.schemas.pairs import MsgCreate, MsgUpdate


router = APIRouter(prefix='/dialogs', tags=['Dialogs'])


@router.post("/message", tags=['MethodsForDirectAccess'])
async def create_msg(message_obj: MsgCreate):
    return await DialogController.create_msg(message_obj)


@router.put("/message/{msg_id}", tags=['MethodsForDirectAccess'])
async def update_msg(msg_id: int, message_obj: MsgUpdate):
    return await DialogController.update_msg(msg_id, message_obj)


@router.get("/", response_model=List)
async def get_user_dialogs(curr_user: dict = Depends(get_current_user)):
    return await DialogController.get_user_dialogs(curr_user)
