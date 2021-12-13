from fastapi import APIRouter

from src.db.init_db import create_tables
from src.routers import users, auth


router = APIRouter()

router.include_router(users.router)
router.include_router(auth.router)


@router.get("/init_db")
def init():
    create_tables()
