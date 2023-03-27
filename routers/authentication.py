from fastapi import  APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.authmodel import auth_login


router = APIRouter()

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    return auth_login(request)