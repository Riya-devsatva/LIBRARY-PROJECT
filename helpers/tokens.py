from fastapi import HTTPException, status, Depends
from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from models.authmodel import TokenData
from fastapi import Request
from helpers.database import user_collection
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_token(request: Request, token: str = Depends(oauth2_scheme), ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

        # for getting logged in user data
        user_info = user_collection.find_one({"email": email})
        request.state.user_info = user_info

        
    except JWTError:
        raise credentials_exception