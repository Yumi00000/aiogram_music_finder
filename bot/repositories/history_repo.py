from models import HistoryModel
import datetime
from bot.core.database import sessionmaker
from sqlalchemy import select

async def create_history(user_id, song_id):

    """Create a new history record in the database."""

    if await get_history_by_user_song(user_id, song_id):
        return None
    new_history = HistoryModel(
            user_id=user_id,
            song_id=song_id,
            recognized_at=datetime.datetime.utcnow()
        )
    async with sessionmaker() as session:
            async with session.begin():
                session.add(new_history)

    return new_history.id


async def get_history_by_user_id(user_id):
    """Retrieve history records from the database by user ID."""
    async with sessionmaker() as session:
        result = await session.execute(
            select(HistoryModel).where(HistoryModel.user_id == user_id)
        )
        history = result.scalars().all()
        return history


async def get_history_by_user_song(user_id, song_id):
    """Retrieve history records from the database by user ID and song ID."""
    async with sessionmaker() as session:
        result = await session.execute(
            select(HistoryModel).where(HistoryModel.user_id == user_id, HistoryModel.song_id == song_id)
        )
        history = result.scalars().first()
        return history

