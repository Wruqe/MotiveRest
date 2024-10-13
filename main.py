from flask import Flask, jsonify, request
from flask_cors import CORS
from services.openai_service import generate_chat_response
from utils.middleware import authenticate_supabase_token
from auth.register_user import register_user
from auth.login_user import login_user
from supabase import create_client, Client
from services.filter_service import FilterService  # Import the new filter service
from services.google_maps_service import GoogleMapsService  # Import the Google Maps service


app = Flask(__name__)
CORS(app)
import os

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
def index():
    return jsonify({'message': 'Flask app is running!'})

# Initialize services
google_maps_service = GoogleMapsService()
filter_service = FilterService()

@app.route('/api/activities', methods=['POST'])
def get_activities():
    data = request.json
    print(data)

    # Extract the list of results from the frontend
    results = data.get('results', [])

    # Prepare a list of places for filtering
    places = []

    # Loop through each place in the results and extract the required fields
    for place in results:
        name = place.get('name', 'Unknown')
        price_level = place.get('price_level', 0)  # Default to 0 if not available
        group_size = place.get('group_size', 1)  # Default to 1 if not available
        budget = place.get('budget', 1000)  # Default to 1000 if not available

        # Construct a place object with the relevant fields
        places.append({
            'name': name,
            'price_level': price_level,
            'group_size': group_size,
            'budget': budget,  # Include budget in each place object
            'tags': place.get('types', [])  # Assuming 'tags' is part of the place object
        })

    # Print to debug
    print("Received places:", places)
    for place in places:
        print(f"Tags for place '{place['name']}': {place['tags']}")  # Ensure tags are an array

    # Print the full data for debugging purposes
    print("data", data)

    # Apply filters for budget and group size using your filter service
    filtered_places = filter_service.apply_filters(places, budget, group_size)

    # Print the filtered places
    print("Filtered places:", filtered_places)

    return jsonify({'places': filtered_places})



@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    data = request.json

    print(data)
    # Ensure firstName and lastName are in the request body
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    print(first_name, last_name)

    if not first_name or not last_name:
        return jsonify({"message": "First name and last name are required."}), 400

    # Assuming you have a user_id or email to identify the user
    user_id = data.get('userId') 
    print(user_id)

    if not user_id:
        return jsonify({"message": "User ID is required to update profile."}), 400

    # Update the user's profile in the 'profiles' table (adjust table name if needed)
    try:
        response = supabase.table('profiles').update({
            'first_name': first_name,
            'last_name': last_name
        }).eq('user_id', user_id).execute()

        # Check if the update was successful
        if response.get('status') == 200:
            return jsonify({"message": "Profile updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update profile"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Route for registering a user
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json

    # Ensure email and password are in the request body
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Call the register_user function
    response = register_user(email, password)

    # Return the response as JSON
    return jsonify(response)


#  Route for logging in a user
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    print(data)

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    response = login_user(email, password)
    return jsonify(response)


@app.route('/api/logout', methods=['POST'])
def logout():
    """
    This function logs out the user using Supabase and returns the raw response for inspection.
    """
    try:
        # Call Supabase's sign-out method
        response = supabase.auth.sign_out()

        # Return the raw response for inspection (stringified)
        return jsonify({"response": str(response)}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"message": f"An error occurred during logout: {str(e)}"}), 500
    
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Parse the incoming JSON request body
        data = request.json
        print('Received data:', data)

        # Generate chat response using OpenAI
        response = generate_chat_response(data)
        return jsonify({'message': response})

    except Exception as e:
        # Return any errors as a response
        return jsonify({
            'error': f'Something went wrong. Details: {str(e)}'
        }), 500
    

if __name__ == '__main__':
    app.run(debug=True)
