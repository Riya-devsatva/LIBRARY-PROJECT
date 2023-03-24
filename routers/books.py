from fastapi import APIRouter, HTTPException, status, Depends, Request
from models.bookmodel import BookModel
from helpers.database import books_collection, db
from models.usermodels import UserModel
# from helpers.oauth2 import get_current_user
import helpers.tokens as tokens 

router = APIRouter()


@router.post('/', response_model=BookModel)
def add_book(request: Request, requests: BookModel, current_user: UserModel = Depends(tokens.verify_token)):
    
    # for getting logged in user data
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email address already exists")
        else:
            add_book = books_collection.insert_one(new_book)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot add a new book, only admin can add.")
    return new_book


@router.get('/{book_code}')
def get_book(book_code: int):
    get_book = books_collection.find_one({"book_code": book_code}, {'_id': 0,})
    # print(all_users)
    return get_book


@router.put('/update/{book_code}')
def update_book(book_code: int, request: BookModel):
    print(book_code)
    filter = {"book_code": book_code}
    newvalues = {"$set": {
        "title": request.title,
        "author": request.author,
    }}
    update_book = books_collection.find_one_and_update(filter, newvalues, {'_id': 0,})
    print(update_book)
    
    return update_book

@router.delete('/delete/{book_code}')
def delete_book(request: Request, book_code: int, current_user: UserModel = Depends(tokens.verify_token)):

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