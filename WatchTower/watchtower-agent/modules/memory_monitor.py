import psutil
import requests
from core.event_handler import EventHandler
from core.policies import memory_usage_policy
import datetime

class MemoryMonitor:
    def __init__(self, config):
        self.memory_threshold = config.get('memory_threshold', 80)
        self.server_url = config.get('server_url', 'http://localhost:8000/data')
        self.event_handler = EventHandler()
        self.endpoint = "memory"

    def check_usage(self):
        memory_usage = psutil.virtual_memory().percent
        memory_virtual = psutil.virtual_memory()._asdict()
        message = f'Memory usage is {memory_usage}%'
        timestamp = datetime.datetime.now().isoformat()

        if memory_usage_policy(memory_usage, self.memory_threshold):
            
            data = {
                "timestamp": timestamp,
                "memory_usage": memory_usage,
                "memory_virtual": memory_virtual,
                "message": message
                }
            self.send_data_to_server(data)

    def send_data_to_server(self, data):

        try:
            response = requests.post(url=f'{self.server_url}/{self.endpoint}', json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            self.event_handler.log_event('Server Error', f'Failed to send data to server: {e}')
