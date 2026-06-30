from  app.services.agents.state import ClaimState
from app.services.llm_service  import generate_claim_review

def review_agent(state : ClaimState):
    prompt = f"""
You are an insurance claim reviewer.

Claim Amount:
₹{state["claim_amount"]}

Claim Description:
{state["claim_description"]}

Policy Context:
{state["policy_context"]}

Analyze the claim and return ONLY in this format:

RECOMMENDATION: APPROVE / REJECT / REVIEW

REASON:
<short reason>

POLICY_SECTION:
<policy section used>
"""

    review = generate_claim_review(prompt)

    state["review"] = review

    recommendation= "REVIEW"

    if "APPROVE" in review.upper():
        recommendation  = "APPROVE"
    elif "REJECT" in review.upper ():
        recommendation= "REJECT"     

    state["recommendation"]= recommendation

    return state