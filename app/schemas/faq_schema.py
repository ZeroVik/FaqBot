# app/schemas/faq_schema.py
from pydantic import BaseModel

class FAQBase(BaseModel):
    question: str

class FAQCreate(FAQBase):
    answer: str

class FAQResponse(FAQBase):
    id: int
    answer: str

    class Config:
        from_attributes = True  # for SQLAlchemy models
