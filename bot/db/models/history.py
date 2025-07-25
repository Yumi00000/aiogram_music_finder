from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.models.base import Base, TimeStampMixin
from bot.db.models.user import UserModel


class SearchHistoryModel(Base):
    __tablename__ = "search_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    artists: Mapped[str] = mapped_column(nullable=False)
    album: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[str] = mapped_column(nullable=False)
    label: Mapped[str] = mapped_column(nullable=False)
    links: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[TimeStampMixin] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                       nullable=False)

    user: Mapped[UserModel] = relationship("UserModel", uselist=False, back_populates="history")
