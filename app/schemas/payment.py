from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    user_id: int
    application_id: int
    application_type: str  # dog or cat
    amount: float


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str