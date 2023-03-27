from fastapi import APIRouter, HTTPException, status, Depends, Request
from models.usermodels import UserModel, add, show, update
from helpers.database import user_collection, db


# from helpers.oauth2 import get_current_user
import helpers.tokens as tokens 


router = APIRouter()

@router.post('', response_model= UserModel)
def create_user(request: UserModel):
    return add(request)

@router.get('/')
def show_user(request: Request, current_user: UserModel = Depends(tokens.verify_token)):
    return show(request)

@router.put('/{email}')
def update_user(email: str, request: UserModel):
   return update(email, request) 

