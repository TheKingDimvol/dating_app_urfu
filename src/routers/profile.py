from fastapi import APIRouter, Depends, UploadFile, File

from src.controllers.profile import ProfileController
from src.middlewares.auth import get_current_user


router = APIRouter(prefix='/profile', tags=['Profile'])


@router.post("/", description='''
    Column names: 
        "name", 
        "password", 
        "date_of_birth", 
        "age", 
        "description", 
        "city", 
        "zodiac_sign", 
        "number", 
        "socionic_type", 
        "sixteen_pers_type"
    ''')
async def update_profile(update_params: dict, curr_user: dict = Depends(get_current_user)):
    return await ProfileController.update(curr_user['id'], update_params)


@router.post("/image")
async def update_profile_image(image: UploadFile = File(...), curr_user: dict = Depends(get_current_user)):
    file_location = f'C:\\Users\\the_k\\Desktop\\dating_app\\src\\images\\{curr_user["phone"]}.jpeg'
    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())
    return {"info": f"file '{image.filename}' saved at '{file_location}'"}


@router.get("/image")
async def get_image(curr_user: dict = Depends(get_current_user)):
    return ProfileController.get_image(curr_user['id'])
