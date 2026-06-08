from fastapi import FastAPI

from app.core.database import Base, engine, supabase

# Auth
from app.routes import auth
from app.routes import claims
from app.routes import google_auth

# Dog Routes
from app.routes.pets_plans import (
    router as dog_plan_router
)

from app.routes.insurance_application import (
    router as dog_insurance_router
)

# Cat Routes
from app.routes.cat_plans import (
    router as cat_plan_router
)

from app.routes.cat_insurance_application import (
    router as cat_insurance_router
)

# Import Models
from app.models.pet_plans import DogPlan
from app.models.insurance_application import InsuranceApplication

from app.models.cat_plans import CatPlan
from app.models.cat_insurance_application import (
    CatInsuranceApplication
)

app = FastAPI(
    title="PetCare Insurance API"
)

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Auth
app.include_router(auth.router)
app.include_router(google_auth.router)

# Claims
app.include_router(claims.router)

# Dog
app.include_router(dog_plan_router)
app.include_router(dog_insurance_router)

# Cat
app.include_router(cat_plan_router)
app.include_router(cat_insurance_router)


@app.get("/")
def home():
    return {
        "message": "PetCare Backend Running"
    }


@app.get("/all_users")
def test():
    data = supabase.table("users").select("*").execute()
    return data.data