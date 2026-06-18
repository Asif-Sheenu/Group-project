from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.core.database import Base


class InsuranceApplication(Base):

    __tablename__ = "insurance_applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    plan_name = Column(String)

    dog_name = Column(String)

    breed = Column(String)

    age = Column(Integer)

    gender = Column(String)

    weight = Column(Float)

    vaccination_status = Column(String)

    existing_disease = Column(String)

    front_image = Column(String)
    side_image = Column(String)
    full_body_image = Column(String)

    vaccination_proof = Column(String)
    medical_record = Column(String)

    status = Column(String, default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)