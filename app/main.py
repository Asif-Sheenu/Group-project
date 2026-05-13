from fastapi import FastAPI
from app.core.database import engine, Base

# import models so SQLAlchemy knows them
from app.models import user  
from app.routes import auth


app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "PetCare backend running"}


