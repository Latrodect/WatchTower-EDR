from fastapi import APIRouter, HTTPException
from utils.http_client import make_request
import os

router = APIRouter()

API_KEY = ""
BASE_URL = "https://www.virustotal.com/api/v3"

@router.get("/virustotal/ip/{ip_address}")
def check_ip(ip_address: str):
    url = f"{BASE_URL}/ip_addresses/{ip_address}"
    headers = {"x-apikey": API_KEY}

    try:
        data = make_request(url, headers)
        return {
            "ip_address": ip_address,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
