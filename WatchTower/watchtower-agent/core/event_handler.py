from pymongo import MongoClient
from config.config_manager import ConfigManager
from core.utils import get_timestamp
import logging

class EventHandler:
    def __init__(self) -> None:
        config = ConfigManager()
        self.client = MongoClient(config.get("mongo_url"))
        self.db = self.client[config.get("db_name")]
        self.collection = self.db[config.get('collection_name')]
        logging.basicConfig(filename=config.get('log_file'), level=logging.INFO)

    def log_event(self, event_type, description):
        event = {
            'timestamp': get_timestamp(),
            'type': event_type,
            'description': description
        }
        self.collection.insert_one(event)