from fastapi import FastAPI
from app.routes import auth
from app.core.database import supabase

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "PetCare backend running"}

@app.get("/test")
def test():
    data = supabase.table("users").select("*").execute()
    return data.data