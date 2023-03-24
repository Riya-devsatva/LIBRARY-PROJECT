from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, Query
from enum import Enum


class LoginModel(BaseModel):
    email: EmailStr = Field()
    password: str = Field()


class TokenData(BaseModel):
    email: EmailStr | None