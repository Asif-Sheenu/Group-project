from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.admin_payment import (
    AdminPaymentListItem,
    AdminPaymentResponse
)

from app.schemas.admin_revenue import RevenueSummary


from app.services.admin_payment_service import (
    get_all_payments,
    get_payment_by_policy,
    get_revenue_summary
)

router = APIRouter(
    prefix="/admin/payments",
    tags=["Admin Payments"]
)


# ==========================================
# Get All Successful Payments (Slim List)
# ==========================================

@router.get(
    "/",
    response_model=List[AdminPaymentListItem]
)
def get_payments(
    db: Session = Depends(get_db)
):

    return get_all_payments(db)


# ==========================================
# Get Payment By Policy Number (Full Detail)
# ==========================================

@router.get(
    "/policy/{policy_number}",
    response_model=AdminPaymentResponse
)
def get_single_payment(
    policy_number: str,
    db: Session = Depends(get_db)
):

    return get_payment_by_policy(
        db,
        policy_number
    )



@router.get(
    "/revenue",
    response_model=RevenueSummary
)
def get_admin_revenue(
    db: Session = Depends(get_db)
):
    return get_revenue_summary(db)





# ////////////////////////////////////////////////////////////////////////////////


# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.core.database import get_db

# from app.schemas.admin_payment import (
#     AdminPaymentResponse,
#     AdminPaymentListResponse
# )

# from app.services.admin_payment_service import (
#     get_all_payments,
#     get_payment_by_policy
# )

# router = APIRouter(
#     prefix="/admin/payments",
#     tags=["Admin Payments"]
# )


# @router.get(
#     "/",
#     response_model=AdminPaymentListResponse
# )
# def get_payments(
#     db: Session = Depends(get_db)
# ):

#     return {
#         "payments": get_all_payments(db)
#     }


# @router.get(
#     "/policy/{policy_number}",
#     response_model=AdminPaymentResponse
# )
# def get_single_payment(
#     policy_number: str,
#     db: Session = Depends(get_db)
# ):

#     return get_payment_by_policy(
#         db,
#         policy_number
#     )