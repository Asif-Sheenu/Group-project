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


# ==========================
# Create Razorpay Order
# ==========================

def create_order(db, request):

    print("\n========== CREATE ORDER ==========")
    print("User ID:", request.user_id)
    print("Application ID:", request.application_id)
    print("Application Type:", request.application_type)
    print("Received Amount:", request.amount)

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

    print("Application Found ✓")

    print(
        "Amount sent to Razorpay (Paise):",
        int(request.amount * 100)
    )

    order = client.order.create({
        "amount": int(request.amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    print("Razorpay Order Created:", order["id"])

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

    print("Payment Saved Successfully")
    print("===============================\n")

    return order


# ==========================
# Verify Payment
# ==========================

def verify_payment(db, request):

    print("\n========== VERIFY PAYMENT ==========")

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

    # Prevent duplicate verification
    if payment.payment_status == "success":

        print("Payment already verified.")
        return payment

    payment.razorpay_payment_id = (
        request.razorpay_payment_id
    )

    payment.payment_status = "success"

    payment.policy_number = (
        "PCI-" +
        uuid.uuid4().hex[:8].upper()
    )

    print("Generated Policy Number:", payment.policy_number)

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

        application.status = "active"

        print("Insurance Activated")

    db.commit()
    db.refresh(payment)

    print("Payment Verification Successful")
    print("=================================\n")

    return payment


# ==========================
# Get User Policy Numbers
# ==========================

def get_user_policy_numbers(db, user_id):

    payments = (
        db.query(Payment)
        .filter(
            Payment.user_id == user_id,
            Payment.payment_status == "success"
        )
        .all()
    )

    return [
        {
            "policy_number": payment.policy_number,
            "application_type": payment.application_type
        }
        for payment in payments
    ]