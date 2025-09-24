from sqlalchemy import Column, Integer, ForeignKey, DATETIME

from bot.core.configure import Base


class HistoryModel(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    recognized_at = Column(DATETIME, nullable=False)