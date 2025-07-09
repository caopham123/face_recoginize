from pydantic import BaseModel, Field
from typing import Optional

class MemberRegister(BaseModel):
    email: str = Field(examples="test@gmail.com")
    name: str = Field(examples="test name")
    image: str = Field()
    class Config:
        json_schema_extra = {
            "email": "test@gmail.com",
            "name": "test name",
            "image": "base64"
        }

class MemberUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    image: Optional[str] = None
    class Config:
        json_schema_extra = {
            "email": "test@gmail.com",
            "name": "test name",
            "image": "base64"
        }

class Image(BaseModel):
    image: str = Field(examples="base64")
    class Config:
        json_schema_extra = {
            "image": "base64"
        }

class MemberChecking(BaseModel):
    email: str = Field(examples="test@gmmail.com")
    name: str = Field(examples="test name")
    class Config:
        json_schema_extra = {
            "email": "test@gmail.com",
            "name": "test name",
        }