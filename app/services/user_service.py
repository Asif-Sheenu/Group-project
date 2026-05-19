from app.core.database import supabase


def get_user_by_email(email: str):
    response = supabase.table("users") \
        .select("*") \
        .eq("email", email) \
        .execute()
    
    return response.data


def create_user(user_data: dict):
    response = supabase.table("users") \
        .insert(user_data) \
        .execute()
    
    return response.data