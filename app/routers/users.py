from fastapi import APIRouter,Depends, HTTPException
from models import User
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from dependencies import get_database

router = APIRouter()


@router.get("/users/", response_model=List[User])
async def get_users(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Fetch all users from the database.
    """
    users_collection = db.users  # Replace 'users' with your collection name
    users = []
    async for user in users_collection.find():
        user["_id"] = str(user["_id"])  # Convert ObjectId to string if needed
        users.append(User(**user))
    return users

@router.post("/user/", response_model=User)
async def create_user(user: User, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Create a new user.
    """
    users_collection = db.users  # Replace 'users' with your collection name

    # Check if the user already exists (based on a unique field, e.g., name)
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400, detail=f"User with email '{user.email}' already exists."
        )

    # Insert the new user into the database
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)

    # Retrieve the inserted user
    user_dict["_id"] = str(result.inserted_id)
    return User(**user_dict)



@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}