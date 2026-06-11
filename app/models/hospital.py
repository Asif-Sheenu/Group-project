from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)

    hospital_name = Column(String, nullable=False)

    registration_number = Column(
        String,
        unique=True,
        nullable=False
    )

    contact_person = Column(String)

    phone = Column(
        String,
        unique=True
    )

    address = Column(String)

    city = Column(String)

    state = Column(String)

    pincode = Column(String)


    verification_status = Column(
        String,
        default="verified"
    )

    password_hash = Column(String)

    website_url = Column(String, nullable=True)
    google_maps_url = Column(String, nullable=True)