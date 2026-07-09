from fastapi import HTTPException

from app.models.payment import Payment

from app.models.insurance_application import (
    InsuranceApplication
)

from app.models.cat_insurance_application import (
    CatInsuranceApplication
)

from app.models.pet_plans import DogPlan

from app.models.cat_plans import CatPlan

from app.services.user_service import helper_func


# ==========================================
# Get All Successful Payments (SLIM LIST)
# ==========================================

def get_all_payments(db):

    payments = (
        db.query(Payment)
        .filter(
            Payment.payment_status == "success"
        )
        .order_by(
            Payment.created_at.desc()
        )
        .all()
    )

    results = []

    for payment in payments:

        # --------------------------
        # Get User From Supabase
        # --------------------------

        user = helper_func(
            payment.user_id
        )

        owner_name = (
            user.get("name")
            if user else "Unknown"
        )

        owner_email = (
            user.get("email")
            if user else "Unknown"
        )

        # --------------------------
        # DOG POLICY
        # --------------------------

        if payment.application_type == "dog":

            application = (
                db.query(
                    InsuranceApplication
                )
                .filter(
                    InsuranceApplication.id ==
                    payment.application_id
                )
                .first()
            )

            if not application:
                continue

            plan = (
                db.query(DogPlan)
                .filter(
                    DogPlan.name ==
                    application.plan_name
                )
                .first()
            )

            if not plan:
                continue

            results.append({

                "owner_name": owner_name,

                "email": owner_email,

                "pet_type": "Dog",

                "pet_name": application.dog_name,

                "plan_name": plan.name,

                "premium_amount": plan.premium_amount,

                "policy_number": payment.policy_number,

                "payment_status": payment.payment_status

            })

        # --------------------------
        # CAT POLICY
        # --------------------------

        else:

            application = (
                db.query(
                    CatInsuranceApplication
                )
                .filter(
                    CatInsuranceApplication.id ==
                    payment.application_id
                )
                .first()
            )

            if not application:
                continue

            plan = (
                db.query(CatPlan)
                .filter(
                    CatPlan.name ==
                    application.plan_name
                )
                .first()
            )

            if not plan:
                continue

            results.append({

                "owner_name": owner_name,

                "email": owner_email,

                "pet_type": "Cat",

                "pet_name": application.cat_name,

                "plan_name": plan.name,

                "premium_amount": plan.premium_amount,

                "policy_number": payment.policy_number,

                "payment_status": payment.payment_status

            })

    return results




# ==========================================
# Get Payment By Policy Number (FULL DETAIL)
# ==========================================

def get_payment_by_policy(
    db,
    policy_number
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

    # --------------------------
    # Get User From Supabase
    # --------------------------

    user = helper_func(
        payment.user_id
    )

    owner_name = (
        user.get("name")
        if user else "Unknown"
    )

    owner_email = (
        user.get("email")
        if user else "Unknown"
    )

    # --------------------------
    # DOG POLICY
    # --------------------------

    if payment.application_type == "dog":

        application = (
            db.query(
                InsuranceApplication
            )
            .filter(
                InsuranceApplication.id ==
                payment.application_id
            )
            .first()
        )

        if not application:

            raise HTTPException(
                status_code=404,
                detail="Dog application not found"
            )

        plan = (
            db.query(DogPlan)
            .filter(
                DogPlan.name ==
                application.plan_name
            )
            .first()
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Dog plan not found"
            )

        return {

            "owner_name": owner_name,

            "email": owner_email,

            "pet_type": "Dog",

            "pet_name": application.dog_name,

            "breed": application.breed,

            "age": application.age,

            "gender": application.gender,

            "weight": application.weight,

            "vaccination_status":
                application.vaccination_status,

            "existing_disease":
                application.existing_disease,

            "plan_name": plan.name,

            "premium_amount":
                plan.premium_amount,

            "claim_limit":
                plan.claim_limit,

            "duration_months":
                plan.duration_months,

            "features":
                plan.features,

            "policy_number":
                payment.policy_number,

            "payment_method":
                "Razorpay",

            "razorpay_order_id":
                payment.razorpay_order_id,

            "razorpay_payment_id":
                payment.razorpay_payment_id,

            "payment_status":
                payment.payment_status,

            "policy_status":
                application.status,

            "purchase_date":
                payment.created_at

        }

    # --------------------------
    # CAT POLICY
    # --------------------------

    application = (
        db.query(
            CatInsuranceApplication
        )
        .filter(
            CatInsuranceApplication.id ==
            payment.application_id
        )
        .first()
    )

    if not application:

        raise HTTPException(
            status_code=404,
            detail="Cat application not found"
        )

    plan = (
        db.query(CatPlan)
        .filter(
            CatPlan.name ==
            application.plan_name
        )
        .first()
    )

    if not plan:

        raise HTTPException(
            status_code=404,
            detail="Cat plan not found"
        )

    return {

        "owner_name": owner_name,

        "email": owner_email,

        "pet_type": "Cat",

        "pet_name": application.cat_name,

        "breed": application.breed,

        "age": application.age,

        "gender": application.gender,

        "weight": application.weight,

        "vaccination_status":
            application.vaccination_status,

        "existing_disease":
            application.existing_disease,

        "plan_name": plan.name,

        "premium_amount":
            plan.premium_amount,

        "claim_limit":
            plan.claim_limit,

        "duration_months":
            plan.duration_months,

        "features":
            plan.features,

        "policy_number":
            payment.policy_number,

        "payment_method":
            "Razorpay",

        "razorpay_order_id":
            payment.razorpay_order_id,

        "razorpay_payment_id":
            payment.razorpay_payment_id,

        "payment_status":
            payment.payment_status,

        "policy_status":
            application.status,

        "purchase_date":
            payment.created_at

    }




# ==========================================
# Get Total Revenue Summary (Admin Credits)
# ==========================================

def get_revenue_summary(db):

    payments = (
        db.query(Payment)
        .filter(Payment.payment_status == "success")
        .all()
    )

    total_revenue = 0.0
    total_transactions = 0

    dog_revenue = 0.0
    cat_revenue = 0.0

    for payment in payments:

        total_revenue += payment.amount
        total_transactions += 1

        if payment.application_type == "dog":
            dog_revenue += payment.amount
        else:
            cat_revenue += payment.amount

    return {
        "total_revenue": total_revenue,
        "total_transactions": total_transactions,
        "dog_revenue": dog_revenue,
        "cat_revenue": cat_revenue
    }