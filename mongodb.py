from pymongo import MongoClient
from fastapi import Depends
from src.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)

    def get_database(self, db_name: str):
        return self.client[db_name]

    def close(self):
        self.client.close()

def get_mongo_db(mongo: MongoDB = Depends(MongoDB)):
    db = mongo.get_database(DATABASE_NAME)
    yield db
    mongo.close()
