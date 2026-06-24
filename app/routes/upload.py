from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.database import supabase
import uuid

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


# ==========================
# Upload Dog/Cat Images
# ==========================

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    try:

        file_bytes = await file.read()

        unique_name = f"{uuid.uuid4()}_{file.filename}"

        supabase.storage.from_("pet-images").upload(
            path=unique_name,
            file=file_bytes,
            file_options={
                "content-type": file.content_type
            }
        )

        image_url = supabase.storage.from_(
            "pet-images"
        ).get_public_url(unique_name)

        return {
            "message": "Image uploaded successfully",
            "url": image_url
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================
# Upload Vaccination / Medical Documents
# ==========================

@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    try:

        file_bytes = await file.read()

        unique_name = f"{uuid.uuid4()}_{file.filename}"

        supabase.storage.from_("pet-documents").upload(
            path=unique_name,
            file=file_bytes,
            file_options={
                "content-type": file.content_type
            }
        )

        document_url = supabase.storage.from_(
            "pet-documents"
        ).get_public_url(unique_name)

        return {
            "message": "Document uploaded successfully",
            "url": document_url
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )