import os
import uuid
import razorpay

from dotenv import load_dotenv
from fastapi import HTTPException
from razorpay.errors import SignatureVerificationError

from app.models.payment import Payment
from app.models.insurance_application import InsuranceApplication
from app.models.cat_insurance_application import CatInsuranceApplication
from app.models.pet_plans import DogPlan
from app.models.cat_plans import CatPlan

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
    print("Received Amount (already in paise):", request.amount)

    if request.application_type == "dog":
        application = (
            db.query(InsuranceApplication)
            .filter(InsuranceApplication.id == request.application_id)
            .first()
        )
    elif request.application_type == "cat":
        application = (
            db.query(CatInsuranceApplication)
            .filter(CatInsuranceApplication.id == request.application_id)
            .first()
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid application type")

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    print("Application Found ✓")

    # Flutter already sends amount in paise (premiumAmount * 100).
    # DO NOT multiply by 100 again here.
    amount_in_paise = int(request.amount)
    print("Amount sent to Razorpay (Paise):", amount_in_paise)

    order = client.order.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "payment_capture": 1
    })

    print("Razorpay Order Created:", order["id"])

    payment = Payment(
        user_id=request.user_id,
        application_id=request.application_id,
        application_type=request.application_type,
        amount=request.amount / 100,  # store in rupees for readability
        razorpay_order_id=order["id"],
        payment_status="pending"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    print("Payment Saved Successfully")
    print("===============================\n")

    # Flutter's CreateOrderResponse.fromJson expects exactly these keys.
    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key_id": os.getenv("RAZORPAY_KEY_ID"),
    }


# ==========================
# Verify Payment
# ==========================

def verify_payment(db, request):

    print("\n========== VERIFY PAYMENT ==========")

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": request.razorpay_order_id,
            "razorpay_payment_id": request.razorpay_payment_id,
            "razorpay_signature": request.razorpay_signature
        })
    except SignatureVerificationError:
        print("Signature verification FAILED")
        raise HTTPException(status_code=400, detail="Payment signature verification failed")

    payment = (
        db.query(Payment)
        .filter(Payment.razorpay_order_id == request.razorpay_order_id)
        .first()
    )

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.payment_status == "success":
        print("Payment already verified.")
        return payment

    payment.razorpay_payment_id = request.razorpay_payment_id
    payment.payment_status = "success"
    payment.policy_number = "PCI-" + uuid.uuid4().hex[:8].upper()

    print("Generated Policy Number:", payment.policy_number)

    if payment.application_type == "dog":
        application = (
            db.query(InsuranceApplication)
            .filter(InsuranceApplication.id == payment.application_id)
            .first()
        )
    else:
        application = (
            db.query(CatInsuranceApplication)
            .filter(CatInsuranceApplication.id == payment.application_id)
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
        .filter(Payment.user_id == user_id, Payment.payment_status == "success")
        .all()
    )
    return [
        {"policy_number": p.policy_number, "application_type": p.application_type}
        for p in payments
    ]






def get_payment_detail_by_policy(db, policy_number):

    payment = (
        db.query(Payment)
        .filter(
            Payment.policy_number == policy_number,
            Payment.payment_status == "success"
        )
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )

    if payment.application_type == "dog":

        application = (
            db.query(InsuranceApplication)
            .filter(InsuranceApplication.id == payment.application_id)
            .first()
        )

        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        plan = (
            db.query(DogPlan)
            .filter(DogPlan.name == application.plan_name)
            .first()
        )

        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        pet_type = "Dog"
        pet_name = application.dog_name

    else:

        application = (
            db.query(CatInsuranceApplication)
            .filter(CatInsuranceApplication.id == payment.application_id)
            .first()
        )

        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        plan = (
            db.query(CatPlan)
            .filter(CatPlan.name == application.plan_name)
            .first()
        )

        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        pet_type = "Cat"
        pet_name = application.cat_name

    return {
        "pet_type": pet_type,
        "pet_name": pet_name,
        "plan_name": plan.name,
        "premium_amount": plan.premium_amount,
        "policy_number": payment.policy_number,
        "payment_method": "Razorpay",
        "razorpay_payment_id": payment.razorpay_payment_id,
        "payment_status": payment.payment_status,
        "purchase_date": payment.created_at
    }