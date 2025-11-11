from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.config import settings
from app.schemas.faq_schema import FAQBase, FAQResponse, FAQCreate
from app.models.faq_model import FAQ
from app.services.ai_service import ask_ai
from app.services.hit_service import record_hit, normalize

router = APIRouter(prefix="/faq", tags=["FAQ"])

@router.post("/ask", response_model=FAQResponse)
def ask_question(
    data: FAQBase,
    db: Session = Depends(get_db),
    save: bool = Query(False, description="Force save this Q/A now")
):
    # Check cache first (case-insensitive exact match)
    existing = (
        db.query(FAQ)
        .filter(func.lower(FAQ.question) == normalize(data.question))
        .first()
    )
    if existing:
        record_hit(db, data.question)
        return existing

    # Generate
    ai_answer = ask_ai(data.question)

    # Hit counting
    count = record_hit(db, data.question)

    # Force save OR threshold reached
    if save or count >= settings.SAVE_THRESHOLD:
        new_faq = FAQ(question=data.question, answer=ai_answer)
        db.add(new_faq)
        db.commit()
        db.refresh(new_faq)
        return new_faq

    # Not saved yet; id=0 signals "ephemeral"
    return FAQResponse(id=0, question=data.question, answer=ai_answer)


@router.post("/save", response_model=FAQResponse)
def save_faq(payload: FAQCreate, db: Session = Depends(get_db)):
    dup = (
        db.query(FAQ)
        .filter(func.lower(FAQ.question) == normalize(payload.question))
        .first()
    )
    if dup:
        return dup
    faq = FAQ(question=payload.question, answer=payload.answer)
    db.add(faq); db.commit(); db.refresh(faq)
    return faq
