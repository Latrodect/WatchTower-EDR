from fastapi import FastAPI
from api.endpoints import data_router, security_router

app = FastAPI()

app.include_router(data_router, prefix="/data", tags=["Data"])
app.include_router(security_router, prefix="/security", tags=["Security"])

@app.get("/")
async def root():
    return {"message": "Welcome to WatchTower API"}
