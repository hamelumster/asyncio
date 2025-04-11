import asyncio

import aiohhtp

from models import SwapiPeople, Session, init_orm, close_orm

MAX_CONCURRENT_REQUESTS = 5

async def fetch_data(url: str, session: aiohhtp.ClientSession, key: str = "name") -> str:
    """
    Выполняет GET запрос к указанному URL и возвращает значение:
    для фильмов - title
    для персонажей - name
    """
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return ""
            data = await response.json()
            return data.get("title", "") if key == "title" else data.get("name", "")
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""

async def gather_fields(urls: list, session: aiohhtp.ClientSession, key: str = "name") -> str:
    """
    Выполняет запросы для списка URL и возвращает строку, разделенную через запятую
    """
    results = await asyncio.gather(*[fetch_data(url, session, key) for url in urls])
    return ", ".join(filter(None, results))

