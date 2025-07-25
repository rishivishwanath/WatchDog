from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users = db["subscribers"]

def subscribe_user(chat_id, pairs):
    users.update_one({"chat_id": chat_id}, {"$set": {"pairs": [p.upper() for p in pairs]}}, upsert=True)

def get_users_by_pair(pair):
    return users.find({"pairs": pair.upper()})
