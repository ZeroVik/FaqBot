from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.question_hit_model import QuestionHit

def normalize(q: str) -> str:
    # lowercase, collapse spaces, strip
    return " ".join(q.lower().split())

def record_hit(db: Session, question: str) -> int:
    qn = normalize(question)
    hit = db.query(QuestionHit).filter(QuestionHit.question_norm == qn).first()
    if not hit:
        hit = QuestionHit(question_norm=qn, count=1, last_asked=datetime.now(timezone.utc))
        db.add(hit)
        db.commit()
        db.refresh(hit)
        return hit.count
    hit.count += 1
    hit.last_asked = datetime.now(timezone.utc)
    db.commit()
    return hit.count
