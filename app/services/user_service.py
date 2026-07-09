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


def helper_func(user_id):

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("id", user_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None