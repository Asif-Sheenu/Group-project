from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.wallet import WalletSummary

from app.services.wallet_service import get_pet_wallet

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)


# ==========================================
# Get Wallet Summary For a Single Pet
# ==========================================

@router.get(
    "/{pet_type}/{application_id}",
    response_model=WalletSummary
)
def get_wallet(
    pet_type: str,
    application_id: int,
    db: Session = Depends(get_db)
):
    return get_pet_wallet(db, application_id, pet_type)