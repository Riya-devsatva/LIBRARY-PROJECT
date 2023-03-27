from enum import Enum
from pydantic import BaseModel, Field
from fastapi import  HTTPException, status
from models.usermodels import UserModel
from helpers.database import books_collection, book_loan_collection

class StatusEnumType(str, Enum):
    """ Enum Class For Loan Status """
    GRANTED = "GRANTED"
    REJECTED = "REJECTED"
    INREVIEW = "IN_REVIEW"

class BookLoanModel(BaseModel):
    """ BookLoan Model """
    user: str = Field()
    book_code: str = Field()
    loan_status: StatusEnumType = StatusEnumType.INREVIEW
    accepted_rejected_by: str | None

    class Config:
        """ 
        u are telling Pydantic exactly that "it's OK if I pass a non-dict value, just get the data from object attributes".
        """
        orm_mode = True

def create(request, fetch_requests):
    """ create function """

    logged_user_info: UserModel = request.state.user_info

    create_loan = BookLoanModel(
        user = logged_user_info['email'],
        book_code= fetch_requests.book_code,
        loan_status= fetch_requests.loan_status
    ).dict()

    check_book = books_collection.find_one({"book_code": fetch_requests.book_code})
    if check_book:
        book_loan_collection.insert_one(create_loan)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book Code Doesn't exists")

    return create_loan

def show(email):
    """ Show Email Function"""
    show_loan = book_loan_collection.find_one({"user": email}, {'_id': 0,})
    print(show_loan)
    return show_loan

def update_status(book_code, request, fetch_request):
    """ Update Function """
    logged_user_info: UserModel = request.state.user_info

    filter_query = {"book_code": book_code}
    newvalues = {
        "$set": {
            "loan_status": fetch_request.loan_status,
            "accepted_rejected_by": logged_user_info['email'],
        }
    }

    if logged_user_info['access_type'] == "ADMIN":
        book_loan_collection.update_one(filter_query, newvalues)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot update this, only admin can do this.")
    return 'update_loan'
