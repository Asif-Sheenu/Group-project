from typing import TypedDict


class ClaimState(TypedDict):
    claim_description: str
    claim_amount: float
    policy_context: str
    review: str
    recommendation: str