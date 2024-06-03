from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class MultipleQuestions(DeclarativeBase):
    __tablename__ = 'multiple_questions'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(JSON, nullable=False)
    option1 = Column(String, nullable=False)
    option2 = Column(String, nullable=False)
    option3 = Column(String, nullable=False)
    option4 = Column(String, nullable=False)
    createdAt=Column(DateTime, default=datetime.now)
    updatedAt=Column(DateTime, default=datetime.now)
