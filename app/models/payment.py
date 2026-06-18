from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    application_id = Column(Integer, nullable=False)

    amount = Column(Float, nullable=False)

    razorpay_order_id = Column(String, unique=True)
    razorpay_payment_id = Column(String, nullable=True)

    payment_status = Column(String, default="pending")

    policy_number = Column(String, unique=True, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)