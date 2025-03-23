from fastapi.responses import JSONResponse
from fastapi import status, APIRouter
from api.schema import Member_Register
from api.helpers.commons import stringToRGB
from api.services.face_recognition import add_user

router = APIRouter(
    prefix="/api/v1",
    tags=["FACE RECOGNIZE"],
    responses={}
)

@router.get("/ping")
async def ping():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "pong"})

@router.post("/add_user")
async def add_user_api(item: Member_Register):
    image = stringToRGB(item.face)
    result = add_user(item.id, item.email, item.name, image)
    if result:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "success"})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"mesmsgage": "susscess"})