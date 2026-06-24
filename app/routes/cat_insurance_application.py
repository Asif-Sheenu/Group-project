from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.cat_insurance_application import (
    CatInsuranceApplicationCreate
)

from app.services.cat_insurance_application_service import (
    create_application,
    get_all_applications,
    get_application_by_id
)

router = APIRouter(
    prefix="/cat-insurance-applications",
    tags=["Cat Insurance Applications"]
)


# ==========================
# Create Cat Insurance Application
# ==========================

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


# ==========================
# Get All Cat Applications
# ==========================

@router.get("/")
def get_all_cat_applications(
    db: Session = Depends(get_db)
):

    return get_all_applications(db)


# ==========================
# Get Single Cat Application
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