from pydantic import BaseModel
from typing import List
class DataRequestCPU(BaseModel):
    timestamp: str
    cpu_usage: float
    cpu_stats: dict
    cpu_count: str
    cpu_frequency: dict
    message: str

class DataRequestDisk(BaseModel):
    timestamp: str
    disk_usage: float
    disk_io: dict
    disk_partitions: list
    message: str

class DataRequestNetwork(BaseModel):
    timestamp: str
    network_io: int
    network_stats: dict
    message: str

class DataRequestMemory(BaseModel):
    timestamp: str
    memory_usage: float
    memory_virtual: dict
    message: str

class DataRequestEvent(BaseModel):
    timestamp: str
    event_category: int
    time_generator: str
    source_name: str
    event_id: int
    event_type: int
    event_data: tuple

class DataRequestNetworkTraffic(BaseModel):
    timestamp: str
    source_ip: str
    destination_ip: str
    package_length: int

class DataRequestConnections(BaseModel):
    timestamp: str
    connections: List[dict]
    message: str
