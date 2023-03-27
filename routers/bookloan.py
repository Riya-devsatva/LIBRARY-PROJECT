from fastapi import APIRouter, Depends, Request, HTTPException, status
from models.book_loanmodel import BookLoanModel, create, show, update_status
from models.usermodels import UserModel
import helpers.tokens as tokens 
# from helpers.database import books_collection, book_loan_collection

router = APIRouter()
@router.post('/', response_model=BookLoanModel)
def create_loan(request: Request, fetch_requests: BookLoanModel, current_user: UserModel = Depends(tokens.verify_token)):
    return create(request, fetch_requests)

@router.get('/{email}')
def show_loan(email: str):
    return show(email)

@router.put('/{book_code}')
def accept_reject(book_code: str, request: Request, fetch_request: BookLoanModel, current_user: UserModel = Depends(tokens.verify_token) ):
    return update_status(book_code, request, fetch_request)
    