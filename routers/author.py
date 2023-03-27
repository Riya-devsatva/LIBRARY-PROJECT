from fastapi import APIRouter, Depends, Request
# from models.usermodels import UserModel
from models.authormodel import AuthorModel, create, show
from helpers import tokens

router = APIRouter(dependencies=[Depends(tokens.verify_token)])

@router.get('')
def show_author(request: Request):
    """ Show author information route"""
    return show(request)

@router.post('', response_model=AuthorModel)
def create_author(fetch_requests: AuthorModel):
    """ Create author route"""
    return create(fetch_requests)
    