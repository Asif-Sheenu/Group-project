from datetime import datetime, timezone

from fastapi import HTTPException
from jose import jwt, JWTError

from app.core.jwt_handler import SECRET_KEY, ALGORITHM
from app.models.revoked_token import RevokedToken


# ==========================================
# Decode a token to get its expiry (for storage)
# ==========================================

def _get_token_expiry(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        exp_timestamp = payload.get("exp")

        if not exp_timestamp:
            raise HTTPException(status_code=400, detail="Invalid token")

        return datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ==========================================
# Revoke (blacklist) a single token
# ==========================================

def revoke_token(db, token: str):

    already_revoked = (
        db.query(RevokedToken)
        .filter(RevokedToken.token == token)
        .first()
    )

    if already_revoked:
        return

    expires_at = _get_token_expiry(token)

    revoked = RevokedToken(
        token=token,
        expires_at=expires_at
    )

    db.add(revoked)
    db.commit()


# ==========================================
# Logout: revoke access token (+ refresh token if given)
# ==========================================

def logout_user(db, access_token: str, refresh_token: str = None):

    revoke_token(db, access_token)

    if refresh_token:
        revoke_token(db, refresh_token)

    return {"message": "Logged out successfully"}


# ==========================================
# Check if a token is revoked (use this in protected routes)
# ==========================================

def is_token_revoked(db, token: str) -> bool:

    revoked = (
        db.query(RevokedToken)
        .filter(RevokedToken.token == token)
        .first()
    )

    return revoked is not None