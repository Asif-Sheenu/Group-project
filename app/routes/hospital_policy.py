from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.hospital_policy_service import (
    get_policy_details
)

router = APIRouter(
    prefix="/hospital",
    tags=["Hospital Policy"]
)


# =====================================
# Search Policy by Policy Number
# =====================================

@router.get("/policy/{policy_number}")
def search_policy(
    policy_number: str,
    db: Session = Depends(get_db)
):

    return get_policy_details(
        db,
        policy_number
    )