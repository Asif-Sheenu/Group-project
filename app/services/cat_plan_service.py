from app.models.cat_plans import CatPlan


def create_plan(db, plan_data):

    plan = CatPlan(
        name=plan_data.name,
        duration_months=plan_data.duration_months,
        premium_amount=plan_data.premium_amount,
        claim_limit=plan_data.claim_limit,
        features=plan_data.features
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


def get_all_plans(db):

    return db.query(CatPlan).all()