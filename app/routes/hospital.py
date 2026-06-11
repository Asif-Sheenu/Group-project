from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.hospital import Hospital

from app.core.security import hash_password

from app.schemas.hospital import (
    HospitalCreate,
    HospitalResponse
)

from app.services.hospital_service import (
    create_hospital
)

from app.services.hospital_verification import (
    verify_url
)

router = APIRouter(
    prefix="/hospitals",
    tags=["Hospitals"]
)


@router.post(
    "/register",
    response_model=HospitalResponse
)
async def register_hospital(
    hospital: HospitalCreate,
    db: Session = Depends(get_db)
):


    if hospital.password != hospital.confirm_password:
        raise HTTPException(
        status_code=400,
        detail="Passwords do not match"
    )
    
    # Website OR Google Maps required
    if (
        not hospital.website_url
        and not hospital.google_maps_url
    ):
        raise HTTPException(
            status_code=400,
            detail="Either Website URL or Google Maps URL is required"
        )

    # Check duplicate phone
    existing_phone = db.query(Hospital).filter(
        Hospital.phone == hospital.phone
    ).first()

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone number already registered"
        )

    # Check duplicate registration number
    existing_reg = db.query(Hospital).filter(
        Hospital.registration_number
        == hospital.registration_number
    ).first()

    if existing_reg:
        raise HTTPException(
            status_code=400,
            detail="Registration number already exists"
        )

    # Verify website or maps URL
    verified = False

    if hospital.website_url:
        verified = verify_url(
            hospital.website_url
        )

    if (
        not verified
        and hospital.google_maps_url
    ):
        verified = verify_url(
            hospital.google_maps_url
        )

    if not verified:
        raise HTTPException(
            status_code=400,
            detail="URL is invalid or unreachable"
        )

    # Create hospital
    new_hospital = create_hospital(
        db=db,
        hospital_data=hospital,
        password_hash=hash_password(
        hospital.password
        )
    )

    return new_hospital