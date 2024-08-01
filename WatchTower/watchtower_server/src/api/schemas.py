from pydantic import BaseModel

class DataResponse(BaseModel):
    key: str
    value: str
