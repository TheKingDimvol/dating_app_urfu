from fastapi import APIRouter, Response

router = APIRouter()


# Временно
USERS = [{"username": "Bill"}, {"username": "Bob"}]

@router.get("/users/", tags=["users"])
async def read_users():
    return USERS


@router.get("/users/{user_id}", tags=["users"])
async def read_users(user_id: int, response: Response):
    try:
        return USERS[user_id]
    except IndexError as e:
        response.status_code = 404
        return {
            'msg': "User with that id doesn't exist",
            'details': str(e)
        }
