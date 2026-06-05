from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import UploadFile,File,Form
from app.services.s3_service import upload_file_to_s3
from app.services.imagehash_checker import  generate_image_hash, is_duplicate_image

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


# @router.post("/claims", response_model=ClaimResponse)
# def create_claim(
#     claim: ClaimCreate,
#     db: Session = Depends(get_db)
# ):

#     return create_claim_service(db, claim)

@router.post("/claims",response_model=ClaimResponse)
async def create_claim(pet_id:int=Form(...),amount:int=Form(...),
                       description:str=Form(...),file:UploadFile=File(...)
                       ,db:Session=Depends(get_db)):
    
    content= await file.read()

    # save tmp for hashing 

    temp_path=f"temp_{file.filename}"

    with open(temp_path,"wb")as temp_file:
        temp_file.write(content)

    file.file.seek(0)    
# upload img to  s3 

    image_url=upload_file_to_s3(file.file,file.filename)
    # generate  img hashh 

    image_hash=generate_image_hash(temp_path)


    # create schmas obj 

    claim_data=ClaimCreate(pet_id=pet_id,amount=amount,description=description)


    # save 

    return create_claim_service(db,claim_data,image_url,image_hash)





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