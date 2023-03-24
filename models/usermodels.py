from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, Query
from enum import Enum


class AccessTypeEnum(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class UserModel(BaseModel):

    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field()
    password: str = Field()
    access_type: AccessTypeEnum = AccessTypeEnum.MEMBER

    class Config: 
        orm_mode = True




