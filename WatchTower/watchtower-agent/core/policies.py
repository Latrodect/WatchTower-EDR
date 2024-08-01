def cpu_usage_policy(cpu_usage, threshold):
    """CPU usage policy."""
    return cpu_usage > threshold

def memory_usage_policy(memory_percent, threshold):
    """Memory usage policy."""
    return memory_percent > threshold

def disk_usage_policy(disk_percent, threshold):
    """Disk usage policy."""
    return disk_percent > threshold

def network_traffic_policy(traffic_data, threshold):
    """Network  usage policy."""
    return traffic_data > threshold
