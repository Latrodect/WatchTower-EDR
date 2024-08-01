from config.config_manager import ConfigManager
from core.event_handler import EventHandler
from modules.cpu_monitor import CPUMonitor
from modules.memory_monitor import MemoryMonitor
from modules.disk_monitor import DiskMonitor
from modules.network_monitor import NetworkMonitor

class Monitor:
    def __init__(self) -> None:
        self.config = ConfigManager()
        self.event_handler = EventHandler()
        self.cpu_monitor = CPUMonitor(self.config)
        self.memory_monitor = MemoryMonitor(self.config)
        self.disk_monitor = DiskMonitor(self.config)
        self.network_monitor = NetworkMonitor(self.config)

    def run(self):
        self.cpu_monitor.check_usage()
        self.memory_monitor.check_usage()
        self.disk_monitor.check_usage()
        self.network_monitor.check_traffic()