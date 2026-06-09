from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.core.database import Base


class Pet(Base):

    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    name = Column(String, nullable=False)

    species = Column(String, nullable=False)

    breed = Column(String)

    age = Column(Integer)

    gender = Column(String)

    weight = Column(Float)

    vaccination_status = Column(String)

    existing_disease = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)