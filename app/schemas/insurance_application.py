from pydantic import BaseModel
from typing import Optional


class InsuranceApplicationCreate(BaseModel):

    plan_name: str

    dog_name: str

    breed: str

    age: int

    gender: str

    weight: float

    vaccination_status: str

    existing_disease: str

    front_image: str
    side_image: str
    full_body_image: str

    vaccination_proof: Optional[str] = None
    medical_record: Optional[str] = None


class InsuranceApplicationResponse(BaseModel):

    id: int

    plan_name: str

    dog_name: str

    status: str

    class Config:
        from_attributes = True