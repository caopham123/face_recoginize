from fastapi.responses import JSONResponse
from fastapi import status, APIRouter
from api.schema import Member_Register, Member_Update, Member_Delete, Image
from api.helpers.commons import stringToRGB
from api.services.face_recognition import register_member, del_user, check_image, check_user
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
async def register_api(item: Member_Register):
    image = stringToRGB(item.image)
    result = register_member(item.id, item.email, item.name, image)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success register"})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "failed register"})

@router.put("/update_member")
async def update_api(item: Member_Update):
    result = register_member(item.id, item.email, item.name, item.image)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success update"})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "failed update"})

@router.delete("/delete_member")
async def delete_api(item: Member_Delete):
    result = del_user(item.id)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": f"success delete id: {item.id}"})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "failed delete"})

@router.post("/check_user")
async def check_user_api(
    item: Image,
    _: str = Depends(verify_client)
):
    image = stringToRGB(item.image)
    return check_user(image)

@router.post("/check_image")
async def check_user_api(item: Image):
    image = stringToRGB(item.image)
    return check_image(image)