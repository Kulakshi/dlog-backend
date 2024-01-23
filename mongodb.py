from pymongo import MongoClient
from fastapi import Depends
from src.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME


class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)

    def get_database(self):
        return self.client[DATABASE_NAME]

    def close(self):
        self.client.drop_database(DATABASE_NAME)
        self.client.close()


def get_mongo_db(mongo: MongoDB = Depends(MongoDB)):
    db = mongo.get_database()
    yield db
    mongo.close()
