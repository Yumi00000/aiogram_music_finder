from __future__ import annotations

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.models.base import Base, TimeStampMixin
from bot.db.models.history import SearchHistoryModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[TimeStampMixin] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                       nullable=False)
    history: Mapped[list[SearchHistoryModel]] = relationship("SearchHistoryModel", back_populates="user",
                                                             cascade="all, delete-orphan")
