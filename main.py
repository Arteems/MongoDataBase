from fastapi import FastAPI, HTTPException, status
from typing import Dict
import uvicorn
import aiohttp
from shemas import UserStats, User
from config import settings
from mongo_crud import get_user, add_user, delete_user, update_user


app = FastAPI()

user_stats: Dict[str, UserStats] = {}


@app.get("/stats/{username}", response_model=UserStats)
async def async_get_user_stats(username: str):
    if username in user_stats:
        return user_stats[username]

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{settings.BASE_CODEWARS_URL}/{username}"
            ) as response:
                response.raise_for_status()
                data = await response.json()
                user_stats_obj = UserStats(**data)
                user_stats[username] = user_stats_obj
                return user_stats_obj
        except aiohttp.ClientError as e:
            print(f"Ошибка при получении статистики пользователя: {e}")
            raise HTTPException(
                status_code=404,
                detail=f"Пользователь '{username}' не найден.",
            )


@app.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UserStats)
def create(user: User):
    if get_user(user_id=user.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким ником уже существует",
        )

    return add_user(user)


@app.put(
    "/update_user/{user_id}",
    response_model=UserStats,
    status_code=status.HTTP_201_CREATED,
)
def update(user_id: str, user_update: UserStats):
    user = get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким ником не найден",
        )

    return update_user(user_id=user_id, user_update=user_update)


@app.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: str):
    user = get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=Status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    delete_user(user_id=user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
