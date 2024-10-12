from supabase import create_client, Client
from dotenv import load_dotenv
import os


load_dotenv()
# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_user(email: str, password: str):
    """
    This function registers a user using Supabase authentication.
    """
    try:
        # Use Supabase's sign-up method with email and password
        response = supabase.auth.sign_up({"email": email, "password": password})

        if response.get('user'):
            # Successfully registered the user
            return {
                "message": "User registered successfully",
                "user": response['user']
            }
        else:
            # Return error if registration failed
            return {"message": "Registration failed", "error": response.get('error')}
    except Exception as e:
        # Handle unexpected errors
        return {"message": f"An error occurred during registration: {str(e)}"}
