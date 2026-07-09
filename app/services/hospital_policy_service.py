from fastapi import HTTPException
from app.models.payment import Payment
from app.models.insurance_application import InsuranceApplication
from app.models.cat_insurance_application import CatInsuranceApplication
from app.models.pet_plans import DogPlan
from app.models.cat_plans import CatPlan
from app.models.user import User


def get_policy_details(db, policy_number: str):

    # ==========================
    # Find Payment
    # ==========================

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

    # ==========================
    # Find User
    # ==========================

    user = (
        db.query(User)
        .filter(
            User.id == payment.user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # ==========================
    # DOG POLICY
    # ==========================

    if payment.application_type == "dog":

        application = (
            db.query(InsuranceApplication)
            .filter(
                InsuranceApplication.id ==
                payment.application_id
            )
            .first()
        )

        if not application:
            raise HTTPException(
                status_code=404,
                detail="Dog insurance application not found"
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

            "policy_number": payment.policy_number,

            "payment_status": payment.payment_status,

            "application_type": "dog",

            "user": {

                "id": user.id,

                "email": user.email

            },

            "pet": {

                "name": application.dog_name,

                "breed": application.breed,

                "age": application.age,

                "gender": application.gender,

                "weight": application.weight,

                "vaccination_status": application.vaccination_status,

                "existing_disease": application.existing_disease,

                "status": application.status

            },

            "plan": {

                "name": plan.name,

                "premium_amount": plan.premium_amount,

                "claim_limit": plan.claim_limit,

                "duration_months": plan.duration_months,

                "features": plan.features

            }

        }

    # ==========================
    # CAT POLICY
    # ==========================

    application = (
        db.query(CatInsuranceApplication)
        .filter(
            CatInsuranceApplication.id ==
            payment.application_id
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Cat insurance application not found"
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

        "policy_number": payment.policy_number,

        "payment_status": payment.payment_status,

        "application_type": "cat",

        "user": {

            "id": user.id,

            "email": user.email

        },

        "pet": {

            "name": application.cat_name,

            "breed": application.breed,

            "age": application.age,

            "gender": application.gender,

            "weight": application.weight,

            "vaccination_status": application.vaccination_status,

            "existing_disease": application.existing_disease,

            "status": application.status

        },

        "plan": {

            "name": plan.name,

            "premium_amount": plan.premium_amount,

            "claim_limit": plan.claim_limit,

            "duration_months": plan.duration_months,

            "features": plan.features

        }

    }