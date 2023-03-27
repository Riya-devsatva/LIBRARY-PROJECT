from fastapi import APIRouter,Depends, Request
from models.bookmodel import BookModel, add, show, update, delete
from models.usermodels import UserModel
import helpers.tokens as tokens 

router = APIRouter()

@router.post('/', response_model=BookModel)
def add_book(request: Request, requests: BookModel, current_user: UserModel = Depends(tokens.verify_token)):
    return add(request, requests)

@router.get('/{book_code}')
def get_book(book_code: str):
    return show(book_code)

@router.put('/{book_code}')
def update_book(book_code: str, request: BookModel):
    return update(book_code, request)

@router.delete('/{book_code}')
def delete_book(request: Request, book_code: str, current_user: UserModel = Depends(tokens.verify_token)):
    return delete(request, book_code)
    