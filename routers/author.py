from fastapi import APIRouter, HTTPException, status, Depends, Request
from models.bookmodel import BookLoanModel
from helpers.database import book_loan_collection, books_collection, author_collection
from models.usermodels import UserModel
from models.authormodel import AuthorModel
# from helpers.oauth2 import get_current_user
import helpers.tokens as tokens 

router = APIRouter()

@router.get('/')
def show_author(request: Request, current_user: UserModel = Depends(tokens.verify_token)):
    # all_users = user_collection.find_one({"email": email}, {'_id': 0,})
    all_authors = author_collection.find()
    for document in all_authors:
          print(document)

    # for getting logged in user data
    logged_user_info: UserModel = request.state.user_info
    print("Printing Logged User Information")
    print(logged_user_info['email'])
    # ----------------------------------------------------------------

    return all_authors

@router.post('/', response_model=AuthorModel)
def create_author(request: Request, fetch_requests: AuthorModel, current_user: UserModel = Depends(tokens.verify_token)):

    logged_user_info: UserModel = request.state.user_info

    create_author = AuthorModel(
        name = fetch_requests.name,
        books= fetch_requests.books,
        email= fetch_requests.email,
    ).dict()

    check_author = author_collection.find_one({"email": fetch_requests.email})
    if check_author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author Already exists")
    else:
        add_author = author_collection.insert_one(create_author)

    return create_author

