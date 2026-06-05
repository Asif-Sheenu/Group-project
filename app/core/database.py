from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from supabase import create_client
from dotenv import load_dotenv
import os
print("STEP 1")

load_dotenv()
print("STEP 2")

DATABASE_URL = os.getenv("DATABASE_URL")
print("STEP 3")

engine = create_engine(DATABASE_URL,connect_args={"connect_timeout": 5})
print("STEP 4")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print(DATABASE_URL)
print(SUPABASE_URL)
print(SUPABASE_KEY)
print("STEP 5")
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)        
print("STEP 6")