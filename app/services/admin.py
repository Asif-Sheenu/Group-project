from sqlalchemy.orm import Session
from app.models.user import User
from app.models.insurance_application import InsuranceApplication


def get_all_users(db: Session):
    return db.query(User).all()


def get_all_pets(db: Session):
    return db.query(InsuranceApplication).all()