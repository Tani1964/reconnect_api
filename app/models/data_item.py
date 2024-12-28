from pydantic import BaseModel

class DataItem(BaseModel):
    title: str
    description: str
