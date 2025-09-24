import datetime

from sqlalchemy import select

from models import UserModel
from bot.core.database import sessionmaker


async def create_user(user_id: int, username: str | None) -> None:
    """Create a new user in the database."""
    if not await get_user_by_telegram_id(user_id):

        new_user = UserModel(telegram_id=user_id, username=username, is_active=True, created_at=datetime.datetime.utcnow())
        async with sessionmaker() as session:
            async with session.begin():
                session.add(new_user)
    else:
        await update_user_status(user_id, True)

async def get_user_by_telegram_id(telegram_id: int) -> UserModel | None:
    """Retrieve a user from the database by their Telegram ID."""

    async with sessionmaker() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        user = result.scalars().first()
        return user

async def update_user_status(telegram_id: int, is_active: bool) -> None:
    """Update the active status of a user."""
    async with sessionmaker() as session:
        async with session.begin():
            result = await session.execute(
                select(UserModel).where(UserModel.telegram_id == telegram_id)
            )
            user = result.scalars().first()
            if user:
                user.is_active = is_active
                session.add(user)