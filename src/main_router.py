from fastapi import APIRouter

from src.db.init_db import create_tables
from src.routers import users, auth, pairs, dialogs, websockets, profile

router = APIRouter()

router.include_router(users.router)
router.include_router(auth.router)
router.include_router(pairs.router)
router.include_router(dialogs.router)
router.include_router(profile.router)
router.include_router(websockets.router)


@router.get("/init_db")
def init():
    create_tables()
