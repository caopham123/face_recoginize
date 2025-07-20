from fastapi.responses import JSONResponse
from fastapi import status, APIRouter
from api.schema import MemberRegister, MemberUpdate, Image
from api.helpers.commons import stringToRGB
from api.services.check_member_service import *
from api.config.valid_credential import VALID_CLIENTS
from fastapi import Header, HTTPException, Depends

router = APIRouter(
    prefix="/api/v1",
    tags=["FACE RECOGNIZE"],
    responses={}
)

@router.get("/ping")
async def ping():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "ponggg"})

@router.post("/member")
async def register_api(item: MemberRegister):
    image = stringToRGB(item.image)
    result = register_member(item.email, item.name, image)

    return result

@router.patch("/member/{id}")
async def update_api(id: int, item: MemberUpdate):
    image_arr = None
    if item.image is not None:
        image_arr = stringToRGB(item.image)
    result = modify_member(id, item.email, item.name, image_arr)
    return result

@router.delete("/member/{id}")
async def delete_api(id: int):
    result = del_user(id)
    return result

@router.get("/member/{name}")
async def get_by_name(name:str):
    return search_member_by_name(name)

@router.get("/member/{email}")
async def get_by_email(email:str):
    return search_member_by_email(email)


@router.post("/check_user")
async def check_user_api(
    item: Image
):
    image = stringToRGB(item.image)
    if image is not None:
        return check_user(image)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content= {"msg": "Invalid image (base64)! Please check it again!"}
    )

@router.post("/check_image")
async def check_user_api(item: Image):
    image = stringToRGB(item.image)
    return check_image(image)