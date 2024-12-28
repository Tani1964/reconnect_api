from pydantic import BaseModel
from datetime import datetime
from typing import List
from .data_item import DataItem

class PrivateData(BaseModel):
    data: List[DataItem]  # List of DataItem instances
    created_at: datetime
    updated_at: datetime
