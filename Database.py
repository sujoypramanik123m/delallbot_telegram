# database.py

from pymongo import MongoClient
from config import DB_URL, DB_NAME

client = MongoClient(DB_URL)
db = client[DB_NAME]
chats_collection = db['chats']
users_collection = db['users']

def add_chat(chat_id):
    if not chats_collection.find_one({"chat_id": chat_id}):
        chats_collection.insert_one({"chat_id": chat_id})

def get_all_chats():
    return [chat['chat_id'] for chat in chats_collection.find()]

def add_user(user):
    if not users_collection.find_one({"user_id": user.id}):
        users_collection.insert_one({
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        })
