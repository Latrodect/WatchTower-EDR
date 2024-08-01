from pydantic import BaseModel

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