from sqlalchemy import Column, Integer, String, JSON

from bot.core.configure import Base


class SongModel(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artists = Column(JSON, nullable=True)
    album = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    genres = Column(JSON, nullable=True)
    duration = Column(Integer, nullable=True)
    links = Column(JSON, nullable=True)
    acrid = Column(String, unique=True, nullable=False)