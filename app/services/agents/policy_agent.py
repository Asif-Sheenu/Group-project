from app.services.agents.state import ClaimState
from app.services.rag_service import search_policy_documents

def policy_agent(state:ClaimState):

    results= search_policy_documents(state['claim_description'])

    context = "/n".join(results['documents'][0])

    state["policy_context"]=context

    return state