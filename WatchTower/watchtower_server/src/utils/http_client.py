import requests

def make_request(url: str, headers: dict):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"HTTP Request failed: {e}")
