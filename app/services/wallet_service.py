from fastapi import HTTPException

from app.models.claim import Claim
from app.models.insurance_application import InsuranceApplication
from app.models.cat_insurance_application import CatInsuranceApplication
from app.models.pet_plans import DogPlan
from app.models.cat_plans import CatPlan


# ==========================================
# Get Wallet Summary For a Single Pet's Policy
# ==========================================

def get_pet_wallet(db, application_id, pet_type):

    if pet_type == "dog":

        application = (
            db.query(InsuranceApplication)
            .filter(InsuranceApplication.id == application_id)
            .first()
        )

        if not application:
            raise HTTPException(status_code=404, detail="Dog application not found")

        plan = (
            db.query(DogPlan)
            .filter(DogPlan.name == application.plan_name)
            .first()
        )

        if not plan:
            raise HTTPException(status_code=404, detail="Dog plan not found")

        pet_name = application.dog_name

    elif pet_type == "cat":

        application = (
            db.query(CatInsuranceApplication)
            .filter(CatInsuranceApplication.id == application_id)
            .first()
        )

        if not application:
            raise HTTPException(status_code=404, detail="Cat application not found")

        plan = (
            db.query(CatPlan)
            .filter(CatPlan.name == application.plan_name)
            .first()
        )

        if not plan:
            raise HTTPException(status_code=404, detail="Cat plan not found")

        pet_name = application.cat_name

    else:
        raise HTTPException(status_code=400, detail="Invalid pet_type")

    # --------------------------
    # Claims tied to THIS specific pet's application id only
    # --------------------------

    approved_claims = (
        db.query(Claim)
        .filter(
            Claim.pet_id == application.id,
            Claim.status == "APPROVED"
        )
        .all()
    )

    redeemed = sum(c.amount for c in approved_claims)
    redeemable = plan.claim_limit - redeemed

    if redeemable < 0:
        redeemable = 0.0

    return {
        "application_id": application.id,
        "pet_type": pet_type.capitalize(),
        "pet_name": pet_name,
        "plan_name": plan.name,
        "claim_limit": plan.claim_limit,
        "redeemed_amount": redeemed,
        "redeemable_amount": redeemable
    }