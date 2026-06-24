from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.insurance_application import (
    InsuranceApplicationCreate
)

from app.services.insurance_application_service import (
    create_application,
    get_all_applications,
    get_application_by_id
)

router = APIRouter(
    prefix="/insurance-applications",
    tags=["Insurance Applications"]
)


# ==========================
# Create Dog Insurance Application
# ==========================

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


# ==========================
# Get All Applications
# ==========================

@router.get("/")
def get_all_dog_applications(
    db: Session = Depends(get_db)
):

    return get_all_applications(db)


# ==========================
# Get Single Application
# ==========================

@router.get("/{application_id}")
def get_single_application(
    application_id: int,
    db: Session = Depends(get_db)
):

    application = get_application_by_id(
        db,
        application_id
    )

    if not application:

        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application