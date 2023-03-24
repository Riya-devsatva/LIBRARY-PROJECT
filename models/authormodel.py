from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, Query
from enum import Enum





class AuthorModel(BaseModel):
    name: str = Field()
    # book_code: int = Field()   
    books: list[str] = []
    email: EmailStr = Field()

    class Config: 
        orm_mode = True 
