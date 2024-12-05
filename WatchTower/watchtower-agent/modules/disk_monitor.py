import psutil
import requests
from core.policies import disk_usage_policy
from core.event_handler import EventHandler
import datetime
import os
from rabbitmq.producer import MonitoringProducer

producer = MonitoringProducer()

class DiskMonitor:
    def __init__(self, config):
        self.disk_threshold = config.get("disk_threshold", 80)
        self.event_handler = EventHandler()
        self.server_url = config.get("server_url", "http://localhost:8000/")
        self.endpoint = "disk"
        producer.connect()

    def check_usage(self):
        disk_info = psutil.disk_usage("/")
        disk_part = [part._asdict() for part in psutil.disk_partitions()]
        disk_io = psutil.disk_io_counters()._asdict()
        message = f"Disk usage is {disk_info.percent}%"
        top_dirs = self.get_top_directories('/')
        timestamp = datetime.datetime.now().isoformat()

        if disk_usage_policy(disk_info.percent, self.disk_threshold):
            data = {
                "timestamp": timestamp,
                "disk_usage": disk_info.percent,
                "disk_io": disk_io,
                "disk_partitions": disk_part,
                "top_directories": top_dirs,
                "message": message,
            }
            self.send_data_to_server(data)

    def get_top_directories(self, path, top_n=5):
        dir_sizes = {}
        for root, dirs, files in os.walk(path):
            total_size = sum(
                os.path.getsize(os.path.join(root, name) for name in files)
            )
            dir_sizes[root] = total_size

        sorted_dirs = sorted(dir_sizes.items(), keys=lambda x: x[1], reverse=True)[
            :top_n
        ]
        return [{"directory": d, "size": s} for d, s in sorted_dirs]

    def send_data_to_server(self, data):
        try:
            producer.publish(data)
            response = requests.post(
                url=f"{self.server_url}/{self.endpoint}", json=data
            )
            response.raise_for_status()
        except requests.RequestException as e:
            self.event_handler.log_event(
                "Server Error", f"Failed to send data to server: {e}"
            )
        finally:
            producer.close()
