from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class ShortAnswerQuestions(Base):
    __tablename__ = 'short_answer_questions'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    tendency = Column(String, nullable=False)
    createdAt=Column(DateTime, default=datetime.now)
    updatedAt=Column(DateTime, default=datetime.now)
