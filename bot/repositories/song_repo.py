from sqlalchemy import select

from bot.core.database import sessionmaker
from models import SongModel


async def create_song(release_date: str, title: str | None = None,
                      artists: dict | None = None, album: str | None = None, duration_ms: int | None = None,
                      links: dict | None = None, genres: dict | None = None, acrid: str | None = None) -> SongModel:
    """Create a new song entry in the database."""

    if await find_song_by_acrid(acrid):
        return await find_song_by_acrid(acrid)
    new_song = SongModel(
        album=album,
        title=title,
        artists=artists,
        links=links,
        release_date=release_date,
        genres=genres,
        duration=duration_ms,
        acrid=acrid
    )
    async with sessionmaker() as session:
        async with session.begin():
            session.add(new_song)
        return new_song

async def find_song_by_acrid(acrid: str) -> SongModel | None:
    """Find a song in the database by its ACRID."""
    async with sessionmaker() as session:
        result = await session.execute(
            select(SongModel).where(SongModel.acrid == acrid)
        )
        song = result.scalars().first()
        print(song)
        return song