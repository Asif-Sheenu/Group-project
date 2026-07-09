from pydantic import BaseModel


class RevenueSummary(BaseModel):

    total_revenue: float

    total_transactions: int

    dog_revenue: float

    cat_revenue: float

    class Config:
        from_attributes = True