from fastapi import APIRouter, HTTPException, status, Depends, Request
from models.bookmodel import BookLoanModel
from helpers.database import book_loan_collection, books_collection
from models.usermodels import UserModel
# from helpers.oauth2 import get_current_user
import helpers.tokens as tokens 

router = APIRouter()

@router.get('/{email}')
def show_loan(email: str):
    show_loan = book_loan_collection.find_one({"user": email}, {'_id': 0,})
    print(show_loan)
    return show_loan

@router.post('/', response_model=BookLoanModel)
def create_loan(request: Request, fetch_requests: BookLoanModel, current_user: UserModel = Depends(tokens.verify_token)):

    logged_user_info: UserModel = request.state.user_info

    create_loan = BookLoanModel(
        user = logged_user_info['email'],
        book_code= fetch_requests.book_code,
        loan_status= fetch_requests.loan_status
    ).dict()

    check_book = books_collection.find_one({"book_code": fetch_requests.book_code})
    if check_book:
        add_loan = book_loan_collection.insert_one(create_loan)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book Code Doesn't exists")

    return create_loan


@router.put('/{book_code}')
def accept_reject(book_code: str, request: Request, fetch_request: BookLoanModel, current_user: UserModel = Depends(tokens.verify_token) ):

    logged_user_info: UserModel = request.state.user_info

    filter = {"book_code": book_code}
    newvalues = {
        "$set": {
            "loan_status": fetch_request.loan_status,
            "accepted_rejected_by": logged_user_info['email'],
        }
    }

    if logged_user_info['access_type'] == "ADMIN":
        update_loan = book_loan_collection.update_one(filter, newvalues)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot update this, only admin can do this.")
    

    return 'update_loan'