from pymongo import MongoClient

Mongo_URL = "mongodb://localhost:27017"

client = MongoClient("mongodb://127.0.0.1:27017")


db = client.library
user_collection = db.get_collection('users')
books_collection = db.get_collection('books')
book_loan_collection = db.get_collection('bookloan')
author_collection = db.get_collection('author')

# =================== ALTERNATE METHOD =====================
# db = client["library"]
# msg_collection = db["users"]
