from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.cat_insurance_application import (
    CatInsuranceApplicationCreate
)

from app.services.cat_insurance_application_service import (
    create_application
)

router = APIRouter(
    prefix="/cat-insurance-applications",
    tags=["Cat Insurance Applications"]
)


@router.post("/")
def apply_insurance(
    application_data: CatInsuranceApplicationCreate,
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