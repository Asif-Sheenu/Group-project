from langgraph.graph import StateGraph,START,END
from app.services.agents.policy_agent import policy_agent
from app.services.agents.review_agent import review_agent
from app.services.agents.state import ClaimState
from app.services.agents.human_review_agent import human_review_agent


# humen review 

def review_router(state: ClaimState):

    print("Router Recommendation:", state["recommendation"])

    if state["recommendation"] == "REVIEW":
        return "human_review"

    return END


# ----

graph = StateGraph(ClaimState)

graph.add_node("policy_agent",policy_agent)
graph.add_node("review_agent",review_agent)
graph.add_node("human_review",human_review_agent)


graph.add_edge(START,"policy_agent")
graph.add_edge("policy_agent","review_agent")

# this was the end for a  normal flow  --------
# graph.add_edge("review_agent", END)


graph.add_conditional_edges("review_agent",review_router)

graph.add_edge("human_review",END)


claim_graph = graph.compile()

