from pymongo import MongoClient

from config import Config


class Database:
    def __init__(self):
        self.client = MongoClient(Config.URL_MONGODB)
        self.db = self.client[Config.DATABASE]

    def __del__(self):
        self.client.close()

    def get_collection(self, collection: str):
        return self.db[collection]
