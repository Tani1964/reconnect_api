from typing_extensions import Annotated

from fastapi import Header, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

def get_database() -> AsyncIOMotorDatabase:
    from main import app  # Import the app object to access app.mongodb
    return app.mongodb

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")