from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.pet import (
    PetCreate,
    PetUpdate
)

from app.services.pet_service import (
    create_pet,
    get_all_pets,
    get_pet_by_id,
    update_pet,
    delete_pet
)

router = APIRouter(
    prefix="/pets",
    tags=["Pets"]
)


@router.post("/")
def add_pet(
    pet_data: PetCreate,
    db: Session = Depends(get_db)
):

    pet = create_pet(db, pet_data)

    return {
        "message": "Pet created successfully",
        "data": pet
    }


@router.get("/")
def get_pets(
    db: Session = Depends(get_db)
):

    return get_all_pets(db)


@router.get("/{pet_id}")
def get_pet(
    pet_id: int,
    db: Session = Depends(get_db)
):

    return get_pet_by_id(db, pet_id)


@router.put("/{pet_id}")
def edit_pet(
    pet_id: int,
    pet_data: PetUpdate,
    db: Session = Depends(get_db)
):

    return update_pet(
        db,
        pet_id,
        pet_data
    )


@router.delete("/{pet_id}")
def remove_pet(
    pet_id: int,
    db: Session = Depends(get_db)
):

    return delete_pet(
        db,
        pet_id
    )