from fastapi import APIRouter, HTTPException, status, Depends, Request
import models.usermodels as usermodels
from helpers.database import user_collection, db
from hashing import Hash

# from helpers.oauth2 import get_current_user
import helpers.tokens as tokens 


router = APIRouter()

@router.post('', response_model= usermodels.UserModel)
def create_user(request: usermodels.UserModel):
    new_user = usermodels.UserModel(
        
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
    
# @router.get('/{email}')
# def show_user(email: str):
#     all_users = user_collection.find_one({"email": email}, {'_id': 0,})
#     # print(all_users)
#     return all_users


@router.get('/')
def show_user(request: Request, current_user: usermodels.UserModel = Depends(tokens.verify_token)):
    # all_users = user_collection.find_one({"email": email}, {'_id': 0,})
    all_users = user_collection.find()
    for document in all_users:
          print(document)

    # for getting logged in user data
    logged_user_info: usermodels.UserModel = request.state.user_info
    print("Printing Logged User Information")
    print(logged_user_info['email'])
    # ----------------------------------------------------------------

    return all_users

@router.put('/{email}')
def update_user(email: str, request: usermodels.UserModel):
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

