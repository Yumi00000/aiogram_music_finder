from sqlalchemy import Column, Integer, String

from bot.core.configure import Base


class SongModel(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=True)
    album = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    acr_id = Column(String, unique=True, nullable=False)
