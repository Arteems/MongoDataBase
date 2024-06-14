import asyncio
from aiogram import Bot, Dispatcher, types
from shemas import UserStats
import aiohttp
from aiogram.filters import CommandStart
from shemas import Languages, User
from config import settings

bot = Bot(token=settings.token.get_secret_value())
dp = Dispatcher()


async def async_get_user_stats(username: str) -> UserStats:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.BASE_URL}/stats/{username}") as response:
            response.raise_for_status()
            data = await response.json()
            return UserStats(**data)


async def async_create_user(user: User) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.BASE_URL})/users", json=user.dict()
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return User(**data)


async def update_user(user: User) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"{settings.BASE_URL}/users/{user.id}", json=user.dict()
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return User(**data)


async def async_delete_user(user: User) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{settings.BASE_URL}/users/{user.id}", json=user.dict()
        ) as response:
            response.raise_for_status()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply(
        "Привет! Напишите имя пользователя Codewars, чтобы получить его статистику.",
        parse_mode=types.ParseMode.HTML,
    )


def get_pretty_info(title: str, rank: int, name: str, color: str, score: int) -> str:
    return (
        f"<b>{title}</b>\n"
        f"  Ранг: {rank}\n"
        f"  Имя: {name}\n"
        f"  Цвет: {color}\n"
        f"  Счет: {score}\n"
    )


@dp.message()
async def echo_message(message: types.Message):
    username = message.text
    try:
        user_stats = await async_get_user_stats(username)
        overall = get_pretty_info(
            "Суммарный результат", **user_stats.ranks["overall"].model_dump()
        )
        languages: Languages = user_stats.ranks["languages"]
        languages_stats = "<b>Отдельно по языкам:</b>\n"
        for language, stat in languages.items():
            languages_stats += get_pretty_info(language, **stat.model_dump())
        response = (
            f"<b>Статистика пользователя {user_stats.username}:</b>\n\n"
            f"{overall}\n"
            f"{languages_stats}"
        )
        await message.reply(response, parse_mode=types.ParseMode.HTML)
    except (aiohttp.ClientError, ValueError) as e:
        print(f"Error: {e}")
        await message.reply("Не удалось получить статистику пользователя.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
