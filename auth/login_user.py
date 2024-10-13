from supabase import create_client, Client
from dotenv import load_dotenv
import os


load_dotenv()
# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_user(email: str, password: str):
    """
    This function logs in a user using Supabase authentication.
    """
    try:
        # Use Supabase's sign-in method with email and password
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        # Check if the login was successful (user and session are present)
        if response.user and response.session:
            # Successfully logged in, return the user and token
            return {
                "message": "Login successful",
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "created_at": str(response.user.created_at)
                },
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token
            }
        else:
            # Return error if login failed
            return {"message": "Login failed", "error": response.error.message if response.error else "Unknown error"}
    
    except Exception as e:
        # Handle unexpected errors
        return {"message": f"An error occurred during login: {str(e)}"}
