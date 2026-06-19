from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.database import supabase

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


# ==========================
# Upload Dog/Cat Images
# ==========================

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...)
):

    try:

        file_bytes = await file.read()

        file_name = file.filename

        supabase.storage.from_(
            "pet-images"
        ).upload(
            path=file_name,
            file=file_bytes
        )

        image_url = supabase.storage.from_(
            "pet-images"
        ).get_public_url(
            file_name
        )

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
# Upload Vaccination PDF
# Upload Medical Report PDF
# ==========================

@router.post("/document")
async def upload_document(
    file: UploadFile = File(...)
):

    try:

        file_bytes = await file.read()

        file_name = file.filename

        supabase.storage.from_(
            "pet-documents"
        ).upload(
            path=file_name,
            file=file_bytes
        )

        document_url = supabase.storage.from_(
            "pet-documents"
        ).get_public_url(
            file_name
        )

        return {
            "message": "Document uploaded successfully",
            "url": document_url
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )