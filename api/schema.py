from pydantic import BaseModel, Field
from typing import Optional

class Member_Register(BaseModel):
    id: int = Field(examples=0)
    email: str = Field(examples="test@gmail.com")
    name: str = Field(examples="test name")
    image: str = None
    class Config:
        json_schema_extra = {
            "id": 0,
            "email": "test@gmail.com",
            "name": "test name",
            "image": "base64"
        }

class Member_Update(BaseModel):
    id: int = Field(examples=0)
    email: Optional[str] = None
    name: Optional[str] = None
    image: Optional[str] = None
    class Config:
        json_schema_extra = {
            "id": 0,
            "email": "test@gmail.com",
            "name": "test name",
            "image": "base64"
        }

class Member_Delete(BaseModel):
    id: int = Field(examples=0)
    class Config:
        json_schema_extra = {
            "id": 0
        }

class Image(BaseModel):
    image: str = Field(examples="base64")
    class Config:
        json_schema_extra = {
            "image": "base64"
        }

class Member_Checking(BaseModel):
    email: str = Field(examples="test@gmmail.com")
    id: int = Field(examples=0)
    name: str = Field(examples="test name")
    class Config:
        json_schema_extra = {
            "email": "test@gmail.com",
            "id": 0,
            "name": "test name",
        }