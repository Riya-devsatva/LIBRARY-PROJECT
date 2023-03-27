from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, Query, HTTPException, status
from enum import Enum
from models.usermodels import UserModel
from helpers.database import books_collection

# class StatusEnumType(str, Enum):
#     GRANTED = "GRANTED"
#     REJECTED = "REJECTED"
#     INREVIEW = "IN_REVIEW"


class BookModel(BaseModel):
    title: str = Field()
    author: str = Field()
    book_code: str = Field()
    added_by: str = Field()

# class BookLoanModel(BaseModel):
#     user: str = Field()
#     book_code: str = Field()
#     loan_status: StatusEnumType = StatusEnumType.INREVIEW   
#     accepted_rejected_by: str | None

#     class Config: 
#         orm_mode = True 


def add(request, requests):
    logged_user_info: UserModel = request.state.user_info
    
    new_book = BookModel(
        title= requests.title,
        author = requests.author,
        book_code= requests.book_code,
        added_by = logged_user_info['email'],
    ).dict()

    if logged_user_info['access_type'] == "ADMIN":
        check_book = books_collection.find_one({"book_code": requests.book_code})
        if check_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This book already exists")
        else:
            add_book = books_collection.insert_one(new_book)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot add a new book, only admin can add.")
    return new_book

def show(book_code):
    get_book = books_collection.find_one({"book_code": book_code}, {'_id': 0,})
    return get_book


def update(book_code, request):
    filter = {"book_code": book_code}
    newvalues = {"$set": {
        "title": request.title,
        "author": request.author,
    }}
    update_book = books_collection.find_one_and_update(filter, newvalues, {'_id': 0,})
    print(update_book)
    
    return update_book

def delete(request, book_code):
    logged_user_info: UserModel = request.state.user_info
    
    if logged_user_info['access_type'] == "ADMIN":
        check_book = books_collection.find_one({"book_code": book_code})
        if check_book:
            delete_book = books_collection.delete_one({"book_code": book_code})
            print(delete_book)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book not found")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot add a new book, only admin can add.")
    
    return 'Book Deleted'
