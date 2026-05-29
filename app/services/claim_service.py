from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models.claim import Claim


def create_claim_service(db: Session, claim):

    try:

        new_claim = Claim(
            pet_id=claim.pet_id,
            amount=claim.amount,
            description=claim.description,
            status="PENDING"
        )

        db.add(new_claim)

        db.commit()

        db.refresh(new_claim)

        return new_claim

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


def get_all_claims_service(db: Session):

    try:

        claims = db.query(Claim).all()

        return claims

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


def get_single_claim_service(db: Session, claim_id: int):

    try:

        claim = (
            db.query(Claim)
            .filter(Claim.id == claim_id)
            .first()
        )

        if not claim:

            raise HTTPException(
                status_code=404,
                detail="Claim not found"
            )

        return claim

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


def update_claim_status_service(
    db: Session,
    claim_id: int,
    status: str
):

    try:

        claim = (
            db.query(Claim)
            .filter(Claim.id == claim_id)
            .first()
        )

        if not claim:

            raise HTTPException(
                status_code=404,
                detail="Claim not found"
            )

        claim.status = status

        db.commit()

        db.refresh(claim)

        return claim

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


def delete_claim_service(db: Session, claim_id: int):

    try:

        claim = (
            db.query(Claim)
            .filter(Claim.id == claim_id)
            .first()
        )

        if not claim:

            raise HTTPException(
                status_code=404,
                detail="Claim not found"
            )

        db.delete(claim)

        db.commit()

        return {
            "message": "Claim deleted successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )