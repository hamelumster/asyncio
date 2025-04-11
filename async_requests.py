import asyncio
from datetime import datetime

import aiohttp
from more_itertools import chunked

from models import SwapiPeople, Session, init_orm, close_orm

MAX_CONCURRENT_REQUESTS = 5

async def fetch_data(url: str, session: aiohttp.ClientSession, key: str = "name") -> str:
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

async def gather_fields(urls: list, session: aiohttp.ClientSession, key: str = "name") -> str:
    """
    Выполняет запросы для списка URL и возвращает строку, разделенную через запятую
    """
    results = await asyncio.gather(*[fetch_data(url, session, key) for url in urls])
    return ", ".join(filter(None, results))

async def get_person(person_id: int, session: aiohttp.ClientSession) -> dict:
    """
    Получает
    """
    url = f"https://swapi.dev/api/people/{person_id}/"
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Персонаж с ID {person_id} не найден")
                return None
            data = await response.json()
    except Exception as e:
        print(f"Ошибка при получении персонажа с ID {person_id}: {e}")
        return None

    person = {
        "id": person_id,
        "birth_year": data.get("birth_year", ""),
        "eye_color": data.get("eye_color", ""),
        "gender": data.get("gender", ""),
        "hair_color": data.get("hair_color", ""),
        "height": data.get("height", ""),
        "mass": data.get("mass", ""),
        "name": data.get("name", ""),
        "skin_color": data.get("skin_color", "")
    }

    homeworld = data.get("homeworld")
    if homeworld:
        person["homeworld"] = await fetch_data(homeworld, session, key="name")
    else:
        person["homeworld"] = ""


    # Обработка списков вложенных значений
    person["films"] = await gather_fields(data.get("films", []), session, key="title") if data.get("films") else ""
    person["species"] = await gather_fields(data.get("species", []), session, key="name") if data.get("species") else ""
    person["starships"] = await gather_fields(data.get("starships", []), session, key="name") if data.get("starships") else ""
    person["vehicles"] = await gather_fields(data.get("vehicles", []), session, key="name") if data.get("vehicles") else ""

    return person

async def insert_results(person_data: list):
    """
    Вставляет полученные данные в БД
    """
    async with Session() as session:
        valid_data = [person for person in person_data if person is not None]
        people = [SwapiPeople(**person) for person in valid_data]
        session.add_all(people)
        await session.commit()

async def main():
    await init_orm()
    person_data_list = []
    async with aiohttp.ClientSession() as session:
        for id_chunk in chunked(range(1, 101), MAX_CONCURRENT_REQUESTS):
            tasks = [get_person(person_id, session) for person_id in id_chunk]
            results = await asyncio.gather(*tasks)
            person_data_list.extend(results)
            print(f"Добавлено персонажей: {len(person_data_list)}")
    await insert_results(person_data_list)
    await close_orm()

start = datetime.now()
asyncio.run(main())
print(f"Время выполнения: {datetime.now() - start}")