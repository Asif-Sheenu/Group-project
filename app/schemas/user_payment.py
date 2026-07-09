from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserPaymentDetail(BaseModel):

    pet_type: str

    pet_name: str

    plan_name: str

    premium_amount: float

    policy_number: str

    payment_method: str

    razorpay_payment_id: str

    payment_status: str

    purchase_date: datetime

    class Config:
        from_attributes = True


class UserPaymentListResponse(BaseModel):

    payments: List[UserPaymentDetail]

    total_paid: float

    class Config:
        from_attributes = True