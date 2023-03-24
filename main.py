from fastapi import FastAPI, APIRouter, Depends
from pymongo import MongoClient
from helpers.database import user_collection
from routers import user,books, authentication, bookloan, author
import helpers.tokens as tokens


app = FastAPI()

# for getting logged in user data
restricted_router = APIRouter(dependencies= [Depends(tokens.verify_token)])
# ---------------------------------------------------------------------------------

app.include_router(authentication.router, tags = ['Auth'])
app.include_router(user.router, prefix = '/user', tags=['User'])
app.include_router(books.router,prefix = '/book',tags = ['Book'])
app.include_router(bookloan.router,prefix = '/bookloan', tags = ['Book Loan'])
app.include_router(author.router, prefix = '/author', tags = ['Author'])
