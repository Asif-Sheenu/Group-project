from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ai_claim_review_service import review_claim

router = APIRouter(
    prefix="/ai_review",
    tags=["AI Review"]
)


@router.post("/claim/{claim_id}")
def ai_review(
    claim_id: int,
    db: Session = Depends(get_db)
):

    return review_claim(
        claim_id,
        db
    )