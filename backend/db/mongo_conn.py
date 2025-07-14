# db/mongo_conn.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_mongo_collection():
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("MONGODB_DATABASE", "valuefy")
    collection_name = os.getenv("MONGODB_COLLECTION", "clients")

    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]
