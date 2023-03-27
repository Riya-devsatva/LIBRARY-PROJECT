from fastapi import APIRouter, Depends, Request
from models.book_loanmodel import BookLoanModel, create, show, update_status
# from models.usermodels import UserModel
from helpers import tokens

router = APIRouter(dependencies=[Depends(tokens.verify_token)])

@router.post('', response_model=BookLoanModel)
def create_loan(request: Request, fetch_requests: BookLoanModel):
    """ create loan route """
    return create(request, fetch_requests)

@router.get('/{email}')
def show_loan(email: str):
    """ show loan route """
    return show(email)

@router.put('/{book_code}')
def accept_reject(book_code: str, request: Request, fetch_request: BookLoanModel ):
    """ accept reject route """
    return update_status(book_code, request, fetch_request)
    