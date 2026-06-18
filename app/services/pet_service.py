from fastapi import HTTPException

from app.models.pet import Pet


def create_pet(db, pet_data):

    pet = Pet(

        user_id=1,

        name=pet_data.name,

        species=pet_data.species,

        breed=pet_data.breed,

        age=pet_data.age,

        gender=pet_data.gender,

        weight=pet_data.weight,

        vaccination_status=pet_data.vaccination_status,

        existing_disease=pet_data.existing_disease
    )

    db.add(pet)

    db.commit()

    db.refresh(pet)

    return pet


def get_all_pets(db):

    return db.query(Pet).all()


def get_pet_by_id(db, pet_id):

    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    return pet


def update_pet(db, pet_id, pet_data):

    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    for key, value in pet_data.dict(exclude_unset=True).items():
        setattr(pet, key, value)

    db.commit()

    db.refresh(pet)

    return pet


def delete_pet(db, pet_id):

    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    db.delete(pet)

    db.commit()

    return {"message": "Pet deleted successfully"}