from fastapi.responses import JSONResponse
from fastapi import status, APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["FACE RECOGNIZE"],
    responses={}
)