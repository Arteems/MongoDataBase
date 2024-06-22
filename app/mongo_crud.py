import pymongo
from app.shemas import UserStats
from config import settings


db_client = pymongo.MongoClient(settings.MONGO_URL)

current_db = db_client["pymongodb"]

collection = current_db["users"]


def create_user(user_id: int, user_stats: UserStats) -> UserStats:
    new_user = {"id": user_id, **user_stats.model_dump()}
    collection.insert_one(new_user)
    return get_user(user_id)


def delete_user(user_id: int):
    collection.delete_one({"id": user_id})


def update_user(user_stats: UserStats, user_id: int) -> UserStats:
    return UserStats(
        collection.find_one_and_update(
            {"id": user_id},
            {"$set": user_stats.model_dump()},
        )
    )


def get_user(user_id: int) -> UserStats | None:
    user_data = collection.find_one({"id": user_id})
    return UserStats(**user_data) if user_data else None


def get_user_by_username(username: str) -> UserStats | None:
    user_data = collection.find_one({"username": username})
    return UserStats(**user_data) if user_data else None
