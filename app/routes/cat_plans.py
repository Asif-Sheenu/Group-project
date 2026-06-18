from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.cat_plan import CatPlanCreate

from app.services.cat_plan_service import (
    create_plan,
    get_all_plans
)

router = APIRouter(
    prefix="/cat-plans",
    tags=["Cat Plans"]
)


@router.post("/")
def add_plan(
    plan_data: CatPlanCreate,
    db: Session = Depends(get_db)
):

    return create_plan(
        db,
        plan_data
    )


@router.get("/")
def get_plans(
    db: Session = Depends(get_db)
):

    return get_all_plans(db)