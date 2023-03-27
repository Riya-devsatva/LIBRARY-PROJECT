from fastapi import APIRouter, Depends
from models.usermodels import UserModel, add, show, update
from helpers import tokens

router = APIRouter(dependencies=[Depends(tokens.verify_token)])

@router.post('', response_model= UserModel)
def create_user(request: UserModel):
    """Create a new user route"""
    return add(request)

@router.get('')
def show_user():
    """Show a user route"""
    return show()

@router.put('/{email}')
def update_user(email: str, request: UserModel):
    """ Update a user route """
    return update(email, request)
