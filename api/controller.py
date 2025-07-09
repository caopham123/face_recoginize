from fastapi.responses import JSONResponse
from fastapi import status, APIRouter
from api.schema import MemberRegister, MemberUpdate, Image
from api.helpers.commons import stringToRGB
from api.services.check_member_service import register_member, modify_member, del_user, check_image, check_user
from api.config.valid_credential import VALID_CLIENTS
from fastapi import Header, HTTPException, Depends
import logging

router = APIRouter(
    prefix="/api/v1",
    tags=["FACE RECOGNIZE"],
    responses={}
)

## Method verify client
async def verify_client(
        client_id: str = Header(...,alias="client-id"),
        client_secret: str = Header(...,alias="client-secret")
):
    if client_id not in VALID_CLIENTS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client ID"
        )
    if VALID_CLIENTS[client_id]['secret'] != client_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client secret"
        )
    return client_id

@router.get("/ping")
async def ping():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "pongGG"})

@router.post("/register")
async def register_api(item: MemberRegister):
    image = stringToRGB(item.image)
    result = register_member(item.email, item.name, image)

    return result

@router.put("/update_member/{id}")
async def update_api(id: int, item: MemberUpdate):
    # , _: str = Depends(verify_client)):
    image_arr = None
    if item.image is not None:
        image_arr = stringToRGB(item.image)
    result = modify_member(id, item.email, item.name, image_arr)
    return result

@router.delete("/delete_member/{id}")
async def delete_api(id: int):
    result = del_user(id)
    return result

@router.post("/check_user")
async def check_user_api(
    item: Image
    # ,_: str = Depends(verify_client)
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