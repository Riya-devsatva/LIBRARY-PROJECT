from pydantic import BaseModel, Field
from fastapi import HTTPException, status
from models.usermodels import UserModel
from helpers.database import books_collection

class BookModel(BaseModel):
    """ Book model """
    title: str = Field()
    author: str = Field()
    book_code: str = Field()
    added_by: str = Field()

def add(request, requests):
    """" Add a new Book Function """
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
            books_collection.insert_one(new_book)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot add a new book, only admin can add.")
    return new_book

def show(book_code):
    """ Show a book Function """
    get_book = books_collection.find_one({"book_code": book_code}, {'_id': 0,})
    return get_book


def update(book_code, request):
    """ Update Book Function """
    filter_query = {"book_code": book_code}
    newvalues = {"$set": {
        "title": request.title,
        "author": request.author,
    }}
    update_book = books_collection.find_one_and_update(filter_query, newvalues, {'_id': 0,})
    print(update_book)
    return update_book

def delete(request, book_code):
    """ Delete Function """
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
