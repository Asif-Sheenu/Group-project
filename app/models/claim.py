from sqlalchemy import Column, Integer, Float, String, DateTime , Text
from sqlalchemy.sql import func
from app.core.database import Base


class Claim(Base):

    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)

    pet_id = Column(Integer, nullable=False)

    amount = Column(Float, nullable=False)

    description = Column(String, nullable=False)

    status = Column(String, default="PENDING")

    ai_recommendation = Column(
    String,
    nullable=True
    )

    ai_reason = Column(
        Text,
    nullable=True
    )

    image_url = Column(String, nullable=True)

    image_hash = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )