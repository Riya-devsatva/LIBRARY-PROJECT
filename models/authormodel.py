from pydantic import BaseModel, EmailStr, Field
from fastapi import HTTPException, status
from models.usermodels import UserModel
from helpers.database import author_collection

class AuthorModel(BaseModel):
    name: str = Field()
    # book_code: int = Field()   
    books: list[str] = []
    email: EmailStr = Field()

    class Config: 
        orm_mode = True 

def create(request, fetch_requests):
    logged_user_info: UserModel = request.state.user_info

    create_author = AuthorModel(
        name = fetch_requests.name,
        books= fetch_requests.books,
        email= fetch_requests.email,
    ).dict()

    check_author = author_collection.find_one({"email": fetch_requests.email})
    if check_author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author Already exists")
    else:
        add_author = author_collection.insert_one(create_author)

    return create_author

def show(request):
    # all_users = user_collection.find_one({"email": email}, {'_id': 0,})
    all_authors = author_collection.find()
    for document in all_authors:
          print(document)

    # for getting logged in user data
    logged_user_info: UserModel = request.state.user_info
    print("Printing Logged User Information")
    print(logged_user_info['email'])
    # ----------------------------------------------------------------

    return all_authors
