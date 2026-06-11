from fastapi import APIRouter, HTTPException
from app.schemas.user import GoogleLoginSchema
from app.services.google_service import verify_google_token
from app.core.database import supabase
from app.core.jwt_handler import create_access_token

router = APIRouter(tags=["Google Auth"])


@router.post("/google/login")
def google_login(data: GoogleLoginSchema):

    try:
        user_info = verify_google_token(data.token)

        email = user_info["email"]
        name = user_info.get("name", "")
        google_id = user_info["sub"]

        existing_user = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )

        if not existing_user.data:

            response = (
                supabase.table("users")
                .insert({
                    "name": name,
                    "email": email,
                    "password": "",
                    "role": "user",
                    "google_id": google_id,
                    "auth_provider": "google"
                })
                .execute()
            )

            db_user = response.data[0]

        else:
            db_user = existing_user.data[0]

        token = create_access_token({
            "email": db_user["email"],
            "role": db_user["role"]
        })

        return {
            "message": "Google login successful",
            "access_token": token,
            "user": db_user
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )