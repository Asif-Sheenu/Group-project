from pydantic import BaseModel


class CatPlanCreate(BaseModel):

    name: str

    duration_months: int

    premium_amount: float

    claim_limit: float

    features: str


class CatPlanResponse(CatPlanCreate):

    id: int

    class Config:
        from_attributes = True