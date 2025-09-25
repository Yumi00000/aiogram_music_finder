from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, BigInteger, String

from bot.core.configure import Base


class HistoryModel(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    song_id = Column(String, ForeignKey("songs.acrid"), nullable=False)
    recognized_at = Column(TIMESTAMP, nullable=False)