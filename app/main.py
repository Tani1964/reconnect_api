from fastapi import Depends, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from contextlib import asynccontextmanager
from typing import List
import sys
from pathlib import Path

from dependencies import get_query_token, get_token_header
from internal import admin
from routers import items, users
from models import User


sys.path.append(str(Path(__file__).resolve().parent))

# MongoDB connection URI
MONGO_URI = config("MONGO_URI")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # MongoDB connection URI
    MONGO_URI = config("MONGO_URI")
    
    try:
        # # Establish MongoDB connection
        app.mongodb_client = AsyncIOMotorClient(MONGO_URI)
        app.mongodb = app.mongodb_client.reconnect  # Replace with your database name
        print("Connected to MongoDB!")
        
        # Yield control to FastAPI for request handling
        yield
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e
    finally:
        # Close the MongoDB connection when the app shuts down
        if hasattr(app, "mongodb_client"):
            app.mongodb_client.close()
            print("MongoDB connection closed!")

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(lifespan=lifespan)


   


app.include_router(users.router)
# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}