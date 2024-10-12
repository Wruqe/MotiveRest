from supabase import create_client, Client
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
import os


load_dotenv()
# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def authenticate_supabase_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', None)
        token = auth_header.split(" ")[1] if auth_header else None

        if not token:
            return jsonify({'message': 'Token is missing. Access denied.'}), 401

        # Verify token with Supabase Auth
        try:
            response = supabase.auth.api.get_user(token)  # Use Supabase to verify the token
            if response.user is None:
                return jsonify({'message': 'Invalid or expired token'}), 403

            request.user = response.user  # Attach user info to the request
        except Exception as e:
            return jsonify({'message': f'Token verification failed: {str(e)}'}), 403

        return f(*args, **kwargs)
    
    return decorated
