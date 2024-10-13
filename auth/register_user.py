from supabase import create_client, Client
from flask import Flask, jsonify, request

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

        # Extract relevant information from the response
        user = {
            "id": response.user.id,
            "email": response.user.email,
            "created_at": str(response.user.created_at),
        }
        session = {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in,
            "expires_at": response.session.expires_at
        }

        # Return a JSON-serializable response with user and session info
        return {
            "message": "User registered successfully",
            "user": user,
            "session": session,
            "code": 201  # Return 201 Created status
        }, 

    except Exception as e:
        # Handle unexpected errors and return a JSON-serializable message
        return {"message": f"An error occurred during registration: {str(e)}"}, 500
