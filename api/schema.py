from pydantic import BaseModel, Field
from typing import Optional

class Member_Register(BaseModel):
    id: str = Field(examples="001")
    email: str = Field(examples="test@gmail.com")
    name: str = Field(examples="test name")
    face: list = Field(examples=[])
    class Config:
        schema_extra = {
            "id": "001",
            "email": "test@gmail.com",
            "name": "test name",
            "face": [124, 124, 124]
        }