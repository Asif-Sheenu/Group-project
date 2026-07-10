from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine, supabase

# ==========================
# Auth
# ==========================

from app.routes import auth
from app.routes import claims
from app.routes import google_auth

from app.routes.logout import router as logout_router

# ==========================
# Payment
# ==========================

from app.routes.payment import router as payment_router

from app.routes.wallet import router as wallet_router

# ==========================
# Admin Payment
# ==========================

from app.routes.admin_payment import (
    router as admin_payment_router
)

# ==========================
# Upload
# ==========================

from app.routes.upload import router as upload_router

# ==========================
# Pet & Hospital
# ==========================

from app.routes.pet import router as pet_router
from app.routes.hospital import router as hospital_router

# ==========================
# Hospital Policy Search
# ==========================

from app.routes.hospital_policy import (
    router as hospital_policy_router
)

# ==========================
# RAG
# ==========================

from app.routes import rag

# ==========================
# Dog Routes
# ==========================

from app.routes.pets_plans import (
    router as dog_plan_router
)

from app.routes.insurance_application import (
    router as dog_insurance_router
)

# ==========================
# Cat Routes
# ==========================

from app.routes.cat_plans import (
    router as cat_plan_router
)

from app.routes.cat_insurance_application import (
    router as cat_insurance_router
)

# ==========================
# AI Claim Review
# ==========================

from app.routes import ai_claim_review

# ==========================
# Admin Route
# ==========================

from app.routes import admin

# ==========================
# Import Models
# ==========================

from app.models.pet_plans import DogPlan
from app.models.insurance_application import InsuranceApplication

from app.models.cat_plans import CatPlan
from app.models.cat_insurance_application import (
    CatInsuranceApplication
)

from app.models.payment import Payment

from app.models.pet import Pet
from app.models.hospital import Hospital


print("MAIN STEP 4")


app = FastAPI(
    title="PetCare Insurance API"
)

# ==========================
# CORS Middleware
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Create Database Tables
# ==========================

Base.metadata.create_all(bind=engine)

# ==========================
# Register Routes
# ==========================

# Auth
app.include_router(auth.router)
app.include_router(google_auth.router)

app.include_router(logout_router)

# Pet
app.include_router(pet_router)

# Hospital
app.include_router(hospital_router)

# Hospital Policy Search
app.include_router(hospital_policy_router)

# Claims
app.include_router(claims.router)

# Payment
app.include_router(payment_router)

app.include_router(wallet_router)

# Admin Payments
app.include_router(admin_payment_router)

# Upload
app.include_router(upload_router)

# Dog Plans
app.include_router(dog_plan_router)

# Dog Insurance
app.include_router(dog_insurance_router)

# Cat Plans
app.include_router(cat_plan_router)

# Cat Insurance
app.include_router(cat_insurance_router)

# RAG
app.include_router(rag.router)

# AI Claim Review
app.include_router(ai_claim_review.router)

# Admin
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)


@app.get("/")
def home():
    return {
        "message": "PetCare Backend Running"
    }


@app.get("/all_users")
def test():

    data = (
        supabase
        .table("users")
        .select("*")
        .execute()
    )

    return data.data