from fastapi import APIRouter, Depends, Request
from models.usermodels import UserModel
from models.authormodel import AuthorModel, create, show
import helpers.tokens as tokens 

router = APIRouter()

@router.get('/')
def show_author(request: Request, current_user: UserModel = Depends(tokens.verify_token)):
    return show(request)

@router.post('/', response_model=AuthorModel)
def create_author(request: Request, fetch_requests: AuthorModel, current_user: UserModel = Depends(tokens.verify_token)):
    return create(request, fetch_requests)
    

