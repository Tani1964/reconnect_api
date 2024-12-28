from typing import Optional
from pydantic import BaseModel
from .public_data import PublicData
from .private_data import PrivateData

class User(BaseModel):
    name: str
    email:str
    description: str
    password: str
    public_data: Optional[PublicData]
    private_data: Optional[PrivateData]