from fastapi import APIRouter,Depends, Request
from models.bookmodel import BookModel, add, show, update, delete
# from models.usermodels import UserModel
from helpers import tokens

router = APIRouter(dependencies=[Depends(tokens.verify_token)])

@router.post('', response_model=BookModel)
def add_book(request: Request, requests: BookModel):
    """ Add a new book route """
    return add(request, requests)

@router.get('/{book_code}')
def get_book(book_code: str):
    """ Get a book route """
    return show(book_code)

@router.put('/{book_code}')
def update_book(book_code: str, request: BookModel):
    """ Update a book route """
    return update(book_code, request)

@router.delete('/{book_code}')
def delete_book(request: Request, book_code: str):
    """ delete book route """
    return delete(request, book_code)
    