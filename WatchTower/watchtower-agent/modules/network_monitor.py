import psutil
import requests
from core.policies import network_traffic_policy
from core.event_handler import EventHandler
from rabbitmq.producer import MonitoringProducer

producer = MonitoringProducer()
class NetworkMonitor:
    def __init__(self, config):
        self.traffic_threshold = config.get('traffic_threshold', 1000000)  
        self.event_handler = EventHandler()
        self.server_url = config.get("server_url", "http://localhost:8000/")
        self.endpoint = "network"
        producer.connect()

    def check_usage(self):
        network_stats = psutil.net_io_counters()
        network_if_stats = psutil.net_if_stats()
        message = f'Network usage is {network_stats.bytes_recv}%'

        if network_traffic_policy(network_stats.bytes_recv, self.traffic_threshold):
            data = {
            "timestamp": "string",
            "network_io": network_stats.bytes_recv,
            "network_stats": network_if_stats,
            "message": message
            }
            self.send_data_to_server(data)

    def send_data_to_server(self,data):
        try:
            producer.publish(data)
            response = requests.post(url=f'{self.server_url}/{self.endpoint}', json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            self.event_handler.log_event('Server Error', f'Failed to send data to server: {e}')
        finally:
            producer.close()