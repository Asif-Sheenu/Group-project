from fastapi import UploadFile,APIRouter,File
from app.services.rag_service import store_policy_document,search_policy_documents
from pydantic import BaseModel


router =APIRouter(tags=["RAG"])

@router.post("/upload-policy")
async def upload_policy(file:UploadFile= File(...)):
    temp_path=f"temp_{file.filename}"

    content=await file.read()

    with open(temp_path,"wb") as f:
        f.write(content)

    store_policy_document(temp_path)

    return{"message":"policy uploaded succesfully"}    


class QestionRequest(BaseModel):
    question:str


@router.post("/ask-policy")
def ask_policy(data:QestionRequest):

    results=search_policy_documents(data.question)

    return results
        