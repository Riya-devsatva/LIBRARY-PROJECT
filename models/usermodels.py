from pydantic import BaseModel, EmailStr, Field
from fastapi import HTTPException, status
from enum import Enum
from hashing import Hash
from helpers.database import user_collection

class AccessTypeEnum(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class UserModel(BaseModel):

    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field()
    password: str = Field()
    access_type: AccessTypeEnum = AccessTypeEnum.MEMBER

    class Config: 
        orm_mode = True

def add(request):
    new_user = UserModel(
        
        first_name= request.first_name,
        last_name= request.last_name,
        email= request.email,
        password= Hash.bcrypt(request.password),
        access_type= request.access_type
    ).dict()
    check_user = user_collection.find_one({"email": request.email})
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email address already exists")
    else:
        add_user = user_collection.insert_one(new_user)

    return new_user

def show(request):
    # all_users = user_collection.find_one({"email": email}, {'_id': 0,})
    all_users = user_collection.find()
    for document in all_users:
          print(document)

    # for getting logged in user data
    logged_user_info: UserModel = request.state.user_info
    print("Printing Logged User Information")
    print(logged_user_info['email'])
    # ----------------------------------------------------------------

    return all_users

def update(email, request):
    filter = {"email": email}
    newvalues = {"$set": {
        "first_name": request.first_name,
        "last_name": request.last_name,
        # "email": request.email,
        "password": request.password,

    }}
    update_user = user_collection.update_one(filter, newvalues)
    # cursor = user_collection.find()
    # for record in cursor:
    #     print(record)
    print(update_user)
    
    return 'User updated'