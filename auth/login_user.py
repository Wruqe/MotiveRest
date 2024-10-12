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
        
        if response.get('user'):
            # Successfully logged in, return the user and token
            return {
                "message": "Login successful",
                "user": response['user'],
                "access_token": response['session']['access_token']
            }
        else:
            # Return error if login failed
            return {"message": "Login failed", "error": response.get('error')}
    except Exception as e:
        # Handle unexpected errors
        return {"message": f"An error occurred during login: {str(e)}"}
