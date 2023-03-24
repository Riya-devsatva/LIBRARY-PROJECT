from fastapi import  APIRouter,  HTTPException, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from hashing import Hash
from models.authmodel import LoginModel
from helpers.database import user_collection
import helpers.tokens as tokens 


router = APIRouter()

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):

    check_user = user_collection.find_one({"email": request.username}, {'_id': 0,})

    if not check_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    print(check_user['password'])
    
    if not Hash.verify(check_user['password'], request.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = tokens.create_access_token(
        data = {"sub": check_user['email']}
    )    
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }