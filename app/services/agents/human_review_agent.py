from app.services.agents.state import ClaimState


def human_review_agent(state: ClaimState):

    print("⚠️ Human review required!")

    state["review"] += "\n\nStatus: Sent for Human Review"

    return state