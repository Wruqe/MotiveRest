from supabase import create_client, Client
from flask import Flask, jsonify, request

from dotenv import load_dotenv
import os

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def logout_user():
    """
    This function logs out a user using Supabase authentication.
    """
    try:
        # Use Supabase's sign-out method
        response = supabase.auth.sign_out()
        
        # If the response doesn't return an error, assume success
        if not response.error:
            return {"message": "Logout successful"}
        else:
            # Return error if logout failed
            return {"message": "Logout failed", "error": response.error.message}

    except Exception as e:
        # Handle unexpected errors
        return {"message": f"An error occurred during logout: {str(e)}"}
