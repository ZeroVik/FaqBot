from sqlalchemy.orm import Session
from app.models.faq_model import FAQ
from app.schemas.faq_schema import FAQCreate

def get_faq_by_question(db: Session, question: str):
    return db.query(FAQ).filter(FAQ.question.ilike(f"%{question}%")).first()

def create_faq(db: Session, faq: FAQCreate):
    new_faq = FAQ(question=faq.question, answer=faq.answer)
    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)
    return new_faq

def get_all_faqs(db: Session):
    return db.query(FAQ).all()
