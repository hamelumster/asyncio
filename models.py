import os

from dotenv import load_dotenv
from sqlalchemy import Integer, String, Text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@localhost:5431/{DB_NAME}",
)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(50))
    eye_color: Mapped[str] = mapped_column(String(50))
    films: Mapped[str] = mapped_column(Text)
    gender: Mapped[str] = mapped_column(String(50))
    hair_color: Mapped[str] = mapped_column(String(50))
    height: Mapped[str] = mapped_column(String(50))
    homeworld: Mapped[str] = mapped_column(String(50))
    mass: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    skin_color: Mapped[str] = mapped_column(String(50))
    species: Mapped[str] = mapped_column(Text)
    starships: Mapped[str] = mapped_column(Text)
    vehicles: Mapped[str] = mapped_column(Text)

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose() 