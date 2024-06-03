import os, asyncio
from pymongo.mongo_client import MongoClient
import motor.motor_asyncio
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import certifi


class MongodbService():
    def __init__(self, db_name, collection_name):
        self.url = os.environ.get('MONGODB_URL')
        self.client = MongoClient(self.url, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        self.aclient = motor.motor_asyncio.AsyncIOMotorClient(self.url, tlsCAFile=certifi.where())
        self.db = self.client[db_name]
        self.adb = self.aclient[db_name]
        self.collection = self.db[collection_name]
        self.acollection = self.adb[collection_name]

    def duplicate_check(self, code) -> bool:
        if self.collection.find_one({'code': code}):
            return True
        return False
    
    async def aduplicate_check(self, code) -> bool:
        if await self.acollection.find_one({'code': code}):
            return True
        return False
    
    def find_by_id(self, _id) -> dict:
        return self.collection.find_one({'_id': ObjectId(_id)}, {'_id': 0})
    
    async def afind_by_id(self, _id) -> dict:
        return await self.acollection.find_one({'_id': ObjectId(_id)}, {'_id': 0})
    
    async def aget_top_ten_json(self, lst):
        tasks = []
        for e in lst[:11]:
            tasks.append(asyncio.create_task(self.afind_by_id(e.metadata['_id']))) 
        result = await asyncio.gather(*tasks)
        return result

