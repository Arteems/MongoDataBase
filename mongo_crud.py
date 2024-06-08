from shemas import User
from config import settings

db_client = pymongo.MongoClient(settings.MONGO_URL)

current_db = db_client["pymongodb"]

collection = current_db["users"]


def add_user(user: User):
    collection.insert_one(user.model_dump())


def delete_user(user: User):
    collection.delete_one({"id": user.id})


def update_user(user: User):
    collection.find_one_and_update(
        {"id": user.id}, {"$set": user.model_dump(exclude="id")}
    )


def get_user(user_id: int):
    return collection.find_one({"id": user_id})
