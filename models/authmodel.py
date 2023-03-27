
from pydantic import BaseModel, EmailStr, Field
from fastapi import HTTPException, status
from helpers.database import user_collection
import helpers.tokens as tokens 
from hashing import Hash

class LoginModel(BaseModel):
    email: EmailStr = Field()
    password: str = Field()

class TokenData(BaseModel):
    email: EmailStr | None

def auth_login(request):
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