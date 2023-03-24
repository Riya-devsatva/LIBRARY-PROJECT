from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, Query
from enum import Enum

class StatusEnumType(str, Enum):
    GRANTED = "GRANTED"
    REJECTED = "REJECTED"
    INREVIEW = "IN_REVIEW"


class BookModel(BaseModel):
    title: str = Field()
    author: str = Field()
    book_code: str = Field()
    added_by: str = Field()

class BookLoanModel(BaseModel):
    user: str = Field()
    book_code: str = Field()
    loan_status: StatusEnumType = StatusEnumType.INREVIEW   
    accepted_rejected_by: str | None

    class Config: 
        orm_mode = True 
