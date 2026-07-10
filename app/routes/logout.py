from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.logout import LogoutRequest

from app.services.token_service import logout_user

router = APIRouter(
    tags=["Auth"]
)


# ==========================================
# Logout (works for user, hospital, admin)
# ==========================================

@router.post("/logout")
def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db)
):
    return logout_user(
        db,
        request.access_token,
        request.refresh_token
    )