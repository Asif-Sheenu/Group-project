from pydantic import BaseModel
from typing import Optional


class PetCreate(BaseModel):

    name: str

    species: str

    breed: str

    age: int

    gender: str

    weight: float

    vaccination_status: str

    existing_disease: Optional[str] = None


class PetUpdate(BaseModel):

    name: Optional[str] = None

    species: Optional[str] = None

    breed: Optional[str] = None

    age: Optional[int] = None

    gender: Optional[str] = None

    weight: Optional[float] = None

    vaccination_status: Optional[str] = None

    existing_disease: Optional[str] = None


class PetResponse(BaseModel):

    id: int

    name: str

    species: str

    breed: str

    age: int

    gender: str

    weight: float

    vaccination_status: str

    existing_disease: str | None = None

    class Config:
        from_attributes = True