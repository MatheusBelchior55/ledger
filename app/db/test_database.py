import asyncio

from app.db.database import async_session
from app.db.models import Organization


async def main():
    async with async_session() as session:
        organization = Organization(
            name="Flush Test",
            email="Flushtest@example.com",
        )

        session.add(organization)

        await session.flush()
        await session.commit()
        await session.refresh(organization)


if __name__ == "__main__":
    asyncio.run(main(), loop_factory=lambda: asyncio.SelectorEventLoop())

