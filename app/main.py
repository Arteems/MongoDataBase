from fastapi import FastAPI, status
import uvicorn
import logging
from app.shemas import UserStats, User
from app.exceptions import UserNotFoundHTTPException, UsernameAllreadyExistHTTPException
from app.mongo_crud import (
    create_user,
    get_user_by_username,
    get_user,
    update_user,
    delete_user,
)

app = FastAPI()


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s % (levelname)s: %(message)s"
)


@app.get("/stats", response_model=UserStats)
def get_user_stats(username: str, id: str):
    logging.info(f"Получение статистики пользователя: username={username}, id={id}")
    user_data = get_user_by_username(username)
    if user_data is None:
        logging.info(
            f"Пользователь не найден, создание нового: username={username}, id={id}"
        )
        user = User(id=id, username=username)
        user_data = create_user(user)
        return user_data
    else:
        logging.info(
            f"Пользователь найден, обновление статистики: username={username}, id={user_data.id}"
        )
        return update_user(user_data.id, user_data)


@app.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UserStats)
def create(user: User):
    if get_user_by_username(user.username):
        logging.warning(f"Пользователь с именем {user.username} уже существует")
        raise UsernameAllreadyExistHTTPException
    logging.info(
        f"Создание нового  пользователя: username={user.username}, id={user.id}"
    )
    return create_user(user)


@app.put(
    "/update_user/{user_id}",
    response_model=UserStats,
    status_code=status.HTTP_201_CREATED,
)
def update(user_id: str, user_update: UserStats):
    user = get_user(user_id=user_id)
    if not user:
        logging.warning(f"Пользователь с id {user_id} не найден")
        raise UserNotFoundHTTPException
    logging.info(f"Обновление данных пользователя: user_id={user_id}")
    return update_user(user_id=user_id, user_update=user_update)


@app.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: str):
    user = get_user(user_id=user_id)
    if not user:
        logging.warning(f"Пользователь с id {user_id} не найден")
        raise UserNotFoundHTTPException
    logging.info(f"Удаление пользователя: user_id={user_id}")
    delete_user(user_id=user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
