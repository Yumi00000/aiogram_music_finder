from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DATETIME

from bot.core.configure import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id= Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at= Column(DATETIME, nullable=False)