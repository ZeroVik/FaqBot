from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.faq_schema import FAQBase, FAQResponse
from app.models.faq_model import FAQ
from app.services.ai_service import ask_ai

router = APIRouter(prefix="/faq", tags=["FAQ"])

@router.post("/ask", response_model=FAQResponse)
def ask_question(data: FAQBase, db: Session = Depends(get_db)):
    # Check if the question exists in DB
    existing = db.query(FAQ).filter(FAQ.question.ilike(data.question)).first()
    if existing:
        return existing  # return cached answer

    # Generate AI answer via Ollama
    ai_answer = ask_ai(data.question)

    # Save it to the database
    new_faq = FAQ(question=data.question, answer=ai_answer)
    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)
    return new_faq
