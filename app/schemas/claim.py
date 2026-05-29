from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ClaimStatus(str,Enum):
    PENDING ="PENDING"
    APPROVED ="APPROVED"
    REJECTED="REJECTED"
    UNDER_REVIEW="UNDER_REVIEW"

class ClaimCreate(BaseModel):
    pet_id:int
    amount:float
    description:str

class  ClaimResponse(BaseModel):
     id : int
     pet_id : int
     amount : float
     description: str
     status: ClaimStatus     
     created_at: datetime
     image_hash: str | None = None
     image_url: str | None = None

class ClaimUpdate(BaseModel):
    status: ClaimStatus

