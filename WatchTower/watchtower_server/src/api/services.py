from db.database import MongoFactory
from api.schemas import DataResponse

def insert_data(data: DataResponse, collection) -> bool: 
    mongo_instance = MongoFactory(collection=collection)
    result = mongo_instance.collection.insert_one(data.dict())
    return result.acknowledged


def fetch_data(key: str, collection):
    mongo_instance = MongoFactory(collection=collection)
    data = mongo_instance.collection.find()
    if data:
        return {"key": data["key"], "value": data["value"]}
    return None