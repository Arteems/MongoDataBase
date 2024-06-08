from fastapi import FastAPI, HTTPException, Status
from typing import Dict
import uvicorn
import aiohttp
from shemas import UserStats
from config import settings
from mongo_crud import get_user


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
                status_code=404, detail=f"Пользователь '{username}' не найден."
            )


@app.post("/create_user")
def create_user(user: User):
    if get_user(user_id=user.id):
        raise HTTPException(
            status_code=Status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким ником уже существует",
        )

    new_user = create_user(user_create)
    return new_user


@app.put("/update_user/{user_id}", response_model=User)
def update_user(user_id: str, user_update: UserUpdate):
    user = get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=Status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким ником не найден",
        )

    update_user = update_user(user_id=user_id, user_update=user_update)
    return update_user


@app.delete("/delete_user/{user_id}", status_code=Status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    user = get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=Status.HTTP_204_NOT_FOUND,
            detail="Пользователь не найден",
        )

    delete_user(user_id=user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
