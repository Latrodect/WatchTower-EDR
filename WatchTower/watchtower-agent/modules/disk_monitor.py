import psutil
import requests
from core.policies import disk_usage_policy
from core.event_handler import EventHandler
import datetime

class DiskMonitor:
    def __init__(self, config):
        self.disk_threshold = config.get('disk_threshold', 80)
        self.event_handler = EventHandler()
        self.server_url = config.get("server_url", "http://localhost:8000/")
        self.endpoint = "disk"

    def check_usage(self):
        disk_info = psutil.disk_usage('/')
        disk_part = [part._asdict() for part in psutil.disk_partitions()]
        disk_io = psutil.disk_io_counters()._asdict()
        message = f'Disk usage is {disk_info.percent}%'
        timestamp = datetime.datetime.now().isoformat()

        if disk_usage_policy(disk_info.percent, self.disk_threshold):
            data = {
                "timestamp": timestamp,
                "disk_usage": disk_info.percent,
                "disk_io": disk_io,
                "disk_partitions":disk_part,
                "message": message
                }
            self.send_data_to_server(data)

    def send_data_to_server(self, data):
        try:
            response = requests.post(url=f'{self.server_url}/{self.endpoint}', json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            self.event_handler.log_event('Server Error', f'Failed to send data to server: {e}')