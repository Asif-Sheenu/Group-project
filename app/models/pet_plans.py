from sqlalchemy import Column, Integer, String, Float

from app.core.database import Base


class DogPlan(Base):

    __tablename__ = "dog_plans"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    duration_months = Column(Integer)

    premium_amount = Column(Float)

    claim_limit = Column(Float)

    features = Column(String)