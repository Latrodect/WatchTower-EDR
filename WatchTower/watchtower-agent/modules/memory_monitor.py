import psutil
import requests
from core.event_handler import EventHandler
from core.policies import memory_usage_policy
import datetime
from rabbitmq.producer import MonitoringProducer

producer = MonitoringProducer()

class MemoryMonitor:
    def __init__(self, config):
        self.memory_threshold = config.get("memory_threshold", 80)
        self.server_url = config.get("server_url", "http://localhost:8000/data")
        self.event_handler = EventHandler()
        self.endpoint = "memory"
        producer.connect()

    def check_usage(self):
        memory_usage = psutil.virtual_memory().percent
        memory_virtual = psutil.virtual_memory()._asdict()
        message = f"Memory usage is {memory_usage}%"
        memory_used = memory_virtual["used"] / (1024**3)
        memory_total = memory_virtual["total"] / (1024**3)
        memory_free = memory_virtual["aviable"] / (1024**3)
        top_processes = self.get_top_memory_processes
        timestamp = datetime.datetime.now().isoformat()

        if memory_usage_policy(memory_usage, self.memory_threshold):
            data = {
                "timestamp": timestamp,
                "memory_usage": memory_usage,
                "memory_virtual": memory_virtual,
                "top_processes": top_processes,
                "memory_used": memory_used,
                "memory_total": memory_total,
                "memory_free": memory_free,
                "message": message,
            }
            self.send_data_to_server(data)

    def get_top_memory_processes(self, count=5):
        processes = []
        for proc in psutil.process_iter(["pid", "name", "memory_percent"]):
            try:
                proc_info = proc.info
                processes.append(proc_info)
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

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
