from pymongo import MongoClient
from datetime import datetime
import uuid
from config import *

class Database:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]
        
    def save_trends(self, trends, ip_address):
        document = {
            "_id": str(uuid.uuid4()),
            "nameoftrend1": trends[0],
            "nameoftrend2": trends[1],
            "nameoftrend3": trends[2],
            "nameoftrend4": trends[3],
            "nameoftrend5": trends[4],
            "timestamp": datetime.now(),
            "ip_address": ip_address
        }
        return self.collection.insert_one(document)
        
    def get_latest_trends(self):
        return self.collection.find_one(sort=[("timestamp", -1)])