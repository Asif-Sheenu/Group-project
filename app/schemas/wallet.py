from typing import List

from pydantic import BaseModel


class PetWalletDetail(BaseModel):

    application_id: int

    pet_type: str

    pet_name: str

    plan_name: str

    claim_limit: float

    redeemed_amount: float

    redeemable_amount: float

    class Config:
        from_attributes = True


class WalletSummary(BaseModel):

    application_id: int

    pet_type: str

    pet_name: str

    plan_name: str

    claim_limit: float

    redeemed_amount: float

    redeemable_amount: float

    class Config:
        from_attributes = True