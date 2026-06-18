from pydantic import BaseModel


class DogPlanCreate(BaseModel):

    name: str
    duration_months: int
    premium_amount: float
    claim_limit: float
    features: str


class DogPlanResponse(DogPlanCreate):

    id: int

    class Config:
        from_attributes = True