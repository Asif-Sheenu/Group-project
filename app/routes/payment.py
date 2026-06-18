from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.payment import (
    CreateOrderRequest,
    VerifyPaymentRequest
)

from app.services.payment_service import (
    create_order,
    verify_payment
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/create-order")
def create_payment_order(
    request: CreateOrderRequest,
    db: Session = Depends(get_db)
):
    return create_order(db, request)


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