from sqlalchemy.orm import Session
from app.models.hospital import Hospital

def create_hospital(
    db: Session,
    hospital_data,
    password_hash
):

    hospital = Hospital(
        hospital_name=hospital_data.hospital_name,
        registration_number=hospital_data.registration_number,
        contact_person=hospital_data.contact_person,
        phone=hospital_data.phone,
        address=hospital_data.address,
        city=hospital_data.city,
        state=hospital_data.state,
        pincode=hospital_data.pincode,
        password_hash=password_hash,

        website_url=hospital_data.website_url,
        google_maps_url=hospital_data.google_maps_url,

        verification_status="verified"
        
    )

    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    return hospital