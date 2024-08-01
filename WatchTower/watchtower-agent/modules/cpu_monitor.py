import psutil
import requests
from core.policies import cpu_usage_policy
from core.event_handler import EventHandler
import datetime

class CPUMonitor:
    def __init__(self, config):
        self.cpu_threshold = config.get('cpu_threshold', 80)
        self.event_handler = EventHandler()
        self.server_url = config.get("server_url", "http://localhost:8000/data/store")
        self.endpoint = "cpu"

    def check_usage(self):
        cpu_usage = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
        cpu_count = psutil.cpu_count()
        cpu_stats = psutil.cpu_stats()._asdict() 
        timestamp = datetime.datetime.now().isoformat()
        message = f'CPU usage is {cpu_usage}%, Count is {cpu_count}°C, Frequency is {cpu_freq}'

        if cpu_usage_policy(cpu_usage, self.cpu_threshold):
            data = {
                'timestamp': timestamp,
                'cpu_usage': cpu_usage,
                'cpu_frequency': cpu_freq,
                'cpu_count': cpu_count,
                'cpu_stats': cpu_stats,
                'message': message
            }
            self.send_data_to_server(data)

    def send_data_to_server(self, data):
        try:
            response = requests.post(url=f'{self.server_url}/{self.endpoint}', json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            self.event_handler.log_event('Server Error', f'Failed to send data to server: {e}')
