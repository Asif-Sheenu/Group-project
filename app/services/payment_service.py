import os
import uuid
import razorpay

from dotenv import load_dotenv
from fastapi import HTTPException

from app.models.payment import Payment
from app.models.insurance_application import InsuranceApplication
from app.models.cat_insurance_application import CatInsuranceApplication

load_dotenv()

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)


def create_order(db, request):

    if request.application_type == "dog":

        application = (
            db.query(InsuranceApplication)
            .filter(
                InsuranceApplication.id ==
                request.application_id
            )
            .first()
        )

    elif request.application_type == "cat":

        application = (
            db.query(CatInsuranceApplication)
            .filter(
                CatInsuranceApplication.id ==
                request.application_id
            )
            .first()
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid application type"
        )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    order = client.order.create({
        "amount": int(request.amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    payment = Payment(
        user_id=request.user_id,
        application_id=request.application_id,
        application_type=request.application_type,
        amount=request.amount,
        razorpay_order_id=order["id"],
        payment_status="pending"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return order


def verify_payment(db, request):

    client.utility.verify_payment_signature({
        "razorpay_order_id": request.razorpay_order_id,
        "razorpay_payment_id": request.razorpay_payment_id,
        "razorpay_signature": request.razorpay_signature
    })

    payment = (
        db.query(Payment)
        .filter(
            Payment.razorpay_order_id ==
            request.razorpay_order_id
        )
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    # Duplicate protection
    if payment.payment_status == "success":
        return payment

    payment.razorpay_payment_id = (
        request.razorpay_payment_id
    )

    payment.payment_status = "success"

    payment.policy_number = (
        "PCI-" +
        uuid.uuid4().hex[:8].upper()
    )

    # Activate Insurance

    if payment.application_type == "dog":

        application = (
            db.query(InsuranceApplication)
            .filter(
                InsuranceApplication.id ==
                payment.application_id
            )
            .first()
        )

    else:

        application = (
            db.query(CatInsuranceApplication)
            .filter(
                CatInsuranceApplication.id ==
                payment.application_id
            )
            .first()
        )

    if application:

        # Adjust names to match your model
        application.status = "active"

        # Optional if field exists
        # application.payment_status = "paid"

    db.commit()
    db.refresh(payment)

    return payment