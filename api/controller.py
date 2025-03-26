from fastapi.responses import JSONResponse
from fastapi import status, APIRouter
from api.schema import Member_Register, Member_Update, Member_Delete, Image
from api.helpers.commons import stringToRGB
from api.services.face_recognition import register_member, del_user, check_image, check_user

router = APIRouter(
    prefix="/api/v1",
    tags=["FACE RECOGNIZE"],
    responses={}
)

@router.get("/ping")
async def ping():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "pong"})

@router.post("/register")
async def register_api(item: Member_Register):
    image = stringToRGB(item.img)
    result = register_member(item.id, item.email, item.name, image)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success register"})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "failed register"})

@router.put("/update_member")
async def update_api(item: Member_Update):
    result = register_member(item.id, item.email, item.name, item.img)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success update"})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "failed update"})

@router.delete("/delete_member")
async def delete_api(item: Member_Delete):
    result = del_user(item.id)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success delete"})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "failed delete"})

@router.post("/check_user")
async def check_user_api(item: Image):
    image = stringToRGB(item.image)
    return check_user(image)

@router.post("/check_image")
async def check_user_api(item: Image):
    image = stringToRGB(item.image)
    return check_image(image)