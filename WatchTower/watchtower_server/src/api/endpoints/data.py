from fastapi import APIRouter
from api.models import DataRequestCPU, DataRequestDisk, DataRequestNetwork, DataRequestMemory, DataRequestEvent, DataRequestConnections, DataRequestNetworkTraffic
from api.services import insert_data, fetch_data

router = APIRouter()

@router.post("/store/cpu")
async def store_cpu_data(data: DataRequestCPU):
    result = insert_data(data, "cpu")
    if result:
        return {"status": "success"}
    return {"status": "failed"}

@router.post("/store/disk")
async def store_disk_data(data: DataRequestDisk):
    print(data)
    result = insert_data(data, "disk")
    if result:
        return {"status": "success"}
    return {"status": "failed"}

@router.post("/store/network")
async def store_network_data(data: DataRequestNetwork):
    print(data)
    result = insert_data(data, "network")
    if result:
        return {"status": "success"}
    return {"status": "failed"}

@router.post("/store/memory")
async def store_memory_data(data: DataRequestMemory):
    print(data)
    result = insert_data(data, "memory")
    if result:
        return {"status": "success"}
    return {"status": "failed"}

@router.get("/{key}")
async def retrieve_data(key: str):
    data = fetch_data(key)
    if data:
        return data
    return {"error": "Data not found"}


@router.post("/store/traffic")
async def store_traffic(data: DataRequestNetworkTraffic):
    result = insert_data(data, "traffic")
    if result:
        return {"status": "success"}
    return {"status": "failed"}

@router.post("/store/connections")
async def store_connections(data: DataRequestConnections):
    result = insert_data(data, "connections")
    if result:
        return {"status": "success"}
    return {"status": "failed"}

@router.post("/store/event")
async def store_event(data: DataRequestEvent):
    print(data)
    result = insert_data(data)
    if result:
        return {"status": "success"}
    return {"status": "failed"}
