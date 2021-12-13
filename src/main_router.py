from fastapi import APIRouter
from src.routers import users, auth


router = APIRouter()

router.include_router(users.router)
router.include_router(auth.router)
