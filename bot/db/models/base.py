from __future__ import annotations
import datetime
from typing import Annotated

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=False)]
big_int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=False, type_=BigInteger)]
created_at = Annotated[
    datetime.datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
]


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols: tuple[str, ...] = ()

    def __repr__(self) -> str:
        cols = [
            f"{col}={getattr(self, col)}"
            for idx, col in enumerate(self.__table__.columns.keys())
            if col in self.repr_cols or idx < self.repr_cols_num
        ]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class TimeStampMixin:
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]