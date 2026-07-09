from pydantic import BaseModel


class UserDetails(BaseModel):
    id: int
    email: str


class PetDetails(BaseModel):
    name: str
    breed: str
    age: int
    gender: str
    weight: float
    vaccination_status: str
    existing_disease: str
    status: str


class PlanDetails(BaseModel):
    name: str
    premium_amount: float
    claim_limit: float
    duration_months: int
    features: str


class HospitalPolicyResponse(BaseModel):

    policy_number: str

    payment_status: str

    application_type: str

    user: UserDetails

    pet: PetDetails

    plan: PlanDetails