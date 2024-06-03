from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass

class Politician(Base):
    __tablename__ = 'politicians'
    id = Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name = Mapped[str] = mapped_column(String)
    data = Mapped[str] = mapped_column(String)
    description = Mapped[str] = mapped_column(String)
    createdAt=Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updatedAt=Mapped[datetime] = mapped_column(DateTime, default=datetime.now)