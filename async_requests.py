import aiohhtp

from models import SwapiPeople, Session, init_orm, close_orm

MAX_CONCURRENT_REQUESTS = 5

async def fetch_all_swapi_people(url: str, session: aiohhtp.ClientSession, key: str = "name") -> str:
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return ""
            data = await response.json()
            return data.get("title", "") if key == "title" else data.get("name", "")
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""



