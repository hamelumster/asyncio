import asyncio
from models import init_orm

async def main():
    await init_orm()
    print("Tables created")

if __name__ == "__main__":
    asyncio.run(main())
