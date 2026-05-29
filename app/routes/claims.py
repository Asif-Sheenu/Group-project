from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import UploadFile,File
from app.services.s3_service import upload_file_to_s3


from app.schemas.claim import (
    ClaimCreate,
    ClaimResponse,
    ClaimUpdate
)

from app.services.claim_service import (
    create_claim_service,
    get_all_claims_service,
    get_single_claim_service,
    update_claim_status_service,
    delete_claim_service
)

from app.core.database import get_db

router = APIRouter()


@router.post("/claims", response_model=ClaimResponse)
def create_claim(
    claim: ClaimCreate,
    db: Session = Depends(get_db)
):

    return create_claim_service(db, claim)


@router.get("/all_claims", response_model=list[ClaimResponse])
def get_all_claims(
    db: Session = Depends(get_db)
):

    return get_all_claims_service(db)


@router.get("/claims/{claim_id}", response_model=ClaimResponse)
def get_claim_by_id(
    claim_id: int,
    db: Session = Depends(get_db)
):

    return get_single_claim_service(db, claim_id)


@router.put("/claims/{claim_id}", response_model=ClaimResponse)
def update_claim_status(
    claim_id: int,
    claim: ClaimUpdate,
    db: Session = Depends(get_db)
):

    return update_claim_status_service(
        db,
        claim_id,
        claim.status
    )


@router.delete("/claims/{claim_id}")
def delete_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):

    return delete_claim_service(db, claim_id)

# upload to s3  

@router.post("/upload")
async def upload_image(file:UploadFile=File(...)):

    file_url=upload_file_to_s3(file.file,  file.filename)
    return {"message":"image uploaded succesfully", "image_url":file_url}