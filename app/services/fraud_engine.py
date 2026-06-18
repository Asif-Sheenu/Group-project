def calculate_fraud_score(amount, duplicate_image):
    fraud_score=0
    
    if  duplicate_image:
        fraud_score+=50

    if amount > 5000:
        fraud_score+=20

    return fraud_score        


def get_claim_status(fraud_score):
    if fraud_score >= 70:
        return "UNDER_REVIEW"
    elif fraud_score>=40:
        return "PENDING"
    return "APPROVED"
