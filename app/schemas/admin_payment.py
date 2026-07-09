from datetime import datetime
from typing import List

from pydantic import BaseModel


# ==========================================
# Slim List Response (for admin list view)
# ==========================================

class AdminPaymentListItem(BaseModel):

    owner_name: str

    email: str

    pet_type: str

    pet_name: str

    plan_name: str

    premium_amount: float

    policy_number: str

    payment_status: str

    class Config:
        from_attributes = True


# ==========================================
# Single Payment Response (full detail)
# ==========================================

class AdminPaymentResponse(BaseModel):

    owner_name: str

    email: str

    pet_type: str

    pet_name: str

    breed: str

    age: int

    gender: str

    weight: float

    vaccination_status: str

    existing_disease: str

    plan_name: str

    premium_amount: float

    claim_limit: float

    duration_months: int

    features: str

    policy_number: str

    payment_method: str

    razorpay_order_id: str

    razorpay_payment_id: str

    payment_status: str

    policy_status: str

    purchase_date: datetime

    class Config:
        from_attributes = True


# ==========================================
# Multiple Payments Response (wrapped, optional use)
# ==========================================

class AdminPaymentListResponse(BaseModel):

    payments: List[AdminPaymentListItem]

    class Config:
        from_attributes = True