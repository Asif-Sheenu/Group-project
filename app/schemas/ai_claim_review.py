from pydantic import BaseModel

class ClaimReviewRequest(BaseModel):
    claim_description:str
    claim_amount:float