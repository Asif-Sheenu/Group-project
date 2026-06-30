from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.payment import (
    CreateOrderRequest,
    VerifyPaymentRequest
)

from app.services.payment_service import (
    create_order,
    verify_payment,
    get_user_policy_numbers
)

from app.models.payment import Payment

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# ==========================
# Create Razorpay Order
# ==========================

@router.post("/create-order")
def create_payment_order(
    request: CreateOrderRequest,
    db: Session = Depends(get_db)
):
    return create_order(db, request)


# ==========================
# Verify Razorpay Payment
# ==========================

@router.post("/verify-payment")
def verify_payment_api(
    request: VerifyPaymentRequest,
    db: Session = Depends(get_db)
):
    payment = verify_payment(db, request)

    return {
        "message": "Payment Successful",
        "policy_number": payment.policy_number
    }


# ==========================
# Get User Policy Numbers
# ==========================

@router.get("/user/{user_id}/policy")
def get_user_policy(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_policy_numbers(
        db,
        user_id
    )


# ==========================
# Get Policy Details
# ==========================

@router.get("/policy/{policy_number}")
def get_policy(
    policy_number: str,
    db: Session = Depends(get_db)
):

    payment = (
        db.query(Payment)
        .filter(
            Payment.policy_number == policy_number
        )
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )

    return {
        "policy_number": payment.policy_number,
        "user_id": payment.user_id,
        "application_id": payment.application_id,
        "application_type": payment.application_type,
        "amount": payment.amount,
        "payment_status": payment.payment_status,
        "created_at": payment.created_at
    }