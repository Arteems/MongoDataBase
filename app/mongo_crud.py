import pymongo
from shemas import User, UserStats
from config import settings


db_client = pymongo.MongoClient(settings.MONGO_URL)

current_db = db_client["pymongodb"]

collection = current_db["users"]


def add_user(user: User) -> UserStats:
    collection.insert_one(user.model_dump())
    return get_user(user.id)


def delete_user(user: User):
    collection.delete_one({"id": user.id})


def update_user(user: User) -> UserStats:
    return UserStats(
        collection.find_one_and_update(
            {"id": user.id},
            {"$set": user.model_dump(exclude="id")},
        )
    )


def get_user(user_id: int) -> UserStats:
    return UserStats(collection.find_one({"id": user_id}))
