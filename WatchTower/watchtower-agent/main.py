
import time
from config.config_manager import ConfigManager
from modules.cpu_monitor import CPUMonitor
from modules.memory_monitor import MemoryMonitor
from modules.disk_monitor import DiskMonitor
from modules.network_monitor import NetworkMonitor

def main():
    config = ConfigManager("config/default_config.yaml")

    cpu_monitor = CPUMonitor(config=config)
    memory_monitor = MemoryMonitor(config=config)
    disk_monitor = DiskMonitor(config)
    network_monitor = NetworkMonitor(config=config)

    while True:
        cpu_monitor.check_usage()
        memory_monitor.check_usage()
        disk_monitor.check_usage()
        network_monitor.check_usage()
        time.sleep(config.get('monitor_interval', 60))
        
if __name__ == "__main__":
    main()