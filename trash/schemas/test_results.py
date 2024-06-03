from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from datetime import datetime

Base = declarative_base()

class TestResults(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True, index=True)
    politicianId = Column(Integer, ForeignKey('politicians.id'), unique=True)
    result = Column(JSON)
    createdAt=Column(DateTime, default=datetime.now)
    updatedAt=Column(DateTime, default=datetime.now)

