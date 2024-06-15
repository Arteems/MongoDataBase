from fastapi import FastAPI, status
from typing import Dict
import uvicorn
import aiohttp
from app.shemas import UserStats, User
from config import settings
from app.mongo_crud import get_user, add_user, delete_user, update_user, get_user_by_username
from app.exceptions import UserNotFoundHTTPException, UsernameAllreadyExistHTTPException


app = FastAPI()

user_stats: Dict[str, UserStats] = {}


@app.get("/stats", response_model=UserStats)
async def async_get_user_stats(username: str, id: int):
    user_data = get_user_by_username(username)
    if user_data is None:
        user = User(id = id, username = username)
        add_user(user)

    


@app.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UserStats)
def create(user: User):
    if get_user(user_id=user.id):
        raise UsernameAllreadyExistHTTPException

    return add_user(user)


@app.put(
    "/update_user/{user_id}",
    response_model=UserStats,
    status_code=status.HTTP_201_CREATED,
)
def update(user_id: str, user_update: UserStats):
    user = get_user(user_id=user_id)
    if not user:
        raise UserNotFoundHTTPException

    return update_user(user_id=user_id, user_update=user_update)


@app.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: str):
    user = get_user(user_id=user_id)
    if not user:
        raise UserNotFoundHTTPException

    delete_user(user_id=user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
