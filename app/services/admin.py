from sqlalchemy.orm import Session
from app.models.user import User
from app.models.insurance_application import InsuranceApplication
from app.models.cat_insurance_application import CatInsuranceApplication


def get_all_users(db: Session):
    return db.query(User).all()


def get_all_dogs(db: Session):
    return db.query(InsuranceApplication).all()

def get_all_cats(db: Session):
    return db.query(CatInsuranceApplication).all()