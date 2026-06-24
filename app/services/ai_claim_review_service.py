from sqlalchemy.orm import Session

from app.models.claim import Claim
from app.services.rag_service import search_policy_documents
from app.services.llm_service import generate_claim_review


def review_claim(
    claim_id: int,
    db: Session
):

    claim = db.query(
        Claim
    ).filter(
        Claim.id == claim_id
    ).first()

    if not claim:
        return {
            "error": "Claim not found"
        }

    results = search_policy_documents(
        claim.description
    )

    context = "\n".join(
        results["documents"][0]
    )

    prompt = f"""
You are an insurance claim reviewer.

Claim Description:
{claim.description}

Claim Amount:
₹{claim.amount}

Policy Context:
{context}

Analyze the claim and return ONLY in this format:

RECOMMENDATION: APPROVE / REJECT / REVIEW

REASON:
<short reason>

POLICY_SECTION:
<policy section used>
"""

    review = generate_claim_review(
        prompt
    )

    recommendation = "REVIEW"

    if "APPROVE" in review.upper():
        recommendation = "APPROVE"

    elif "REJECT" in review.upper():
        recommendation = "REJECT"

    claim.ai_recommendation = recommendation
    claim.ai_reason = review

    db.commit()
    db.refresh(claim)
    
    return {
    "claim_id": claim.id,
    "recommendation": recommendation,
    "review": review
}