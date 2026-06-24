import os
import uuid
import razorpay

from dotenv import load_dotenv
from app.models.payment import Payment

load_dotenv()

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)


def create_order(db, request):

    order = client.order.create({
        "amount": int(request.amount * 100),  # paise
        "currency": "INR",
        "payment_capture": 1
    })

    payment = Payment(
        user_id=request.user_id,
        application_id=request.application_id,
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

    if payment:

        payment.razorpay_payment_id = (
            request.razorpay_payment_id
        )

        payment.payment_status = "success"

        payment.policy_number = (
            "PCI-" +
            uuid.uuid4().hex[:8].upper()
        )

        db.commit()
        db.refresh(payment)

    return payment