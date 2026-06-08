from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.insurance_application import (
    InsuranceApplicationCreate
)

from app.services.insurance_application_service import (
    create_application
)

router = APIRouter(
    prefix="/insurance-applications",
    tags=["Insurance Applications"]
)


@router.post("/")
def apply_insurance(
    application_data: InsuranceApplicationCreate,
    db: Session = Depends(get_db)
):

    application = create_application(
        db,
        application_data
    )

    return {
        "message": "Application submitted successfully",
        "data": application
    }