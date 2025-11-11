from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class QuestionHit(Base):
    __tablename__ = "question_hits"

    id = Column(Integer, primary_key=True, index=True)
    question_norm = Column(String, unique=True, index=True, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    last_asked = Column(DateTime, server_default=func.now(), onupdate=func.now())
