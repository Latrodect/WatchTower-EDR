from pydantic import BaseModel
from typing import List


class ProcessInfoCPU(BaseModel):
    pid: int
    name: str
    cpu_percent: float


class ProcessInfoMemory(BaseModel):
    pid: int
    name: str
    memory_percent: float


class DataRequestCPU(BaseModel):
    timestamp: str
    cpu_usage: float
    cpu_stats: dict
    cpu_count: str
    cpu_frequency: dict
    top_processes: List[ProcessInfoCPU]
    message: str


class DataRequestDisk(BaseModel):
    timestamp: str
    disk_usage: float
    disk_io: dict
    disk_partitions: List
    top_directories: List
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
    top_processes: List[ProcessInfoMemory]
    memory_used: str
    memory_total: str
    memory_free: str
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
