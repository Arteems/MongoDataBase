import aiohttp
from config import settings


async def get_codewars_stats(username: str) -> dict | None:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{settings.BASE_CODEWARS_URL}/{username}"
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:  # TODO: Отдельная обработка ошибок
            return None
