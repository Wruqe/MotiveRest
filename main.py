from flask import Flask, jsonify, request
from flask_cors import CORS
from agents.activity_agent import ActivityAgent
from services.openai_service import generate_chat_response
from utils.middleware import authenticate_supabase_token
from auth.register_user import register_user
from auth.login_user import login_user
app = Flask(__name__)
CORS(app)

# Instantiate the activity agent
activity_agent = ActivityAgent()

@app.route('/')
def index():
    return jsonify({'message': 'Flask app is running!'})

@app.route('/api/activities', methods=['POST'])
@authenticate_supabase_token
def get_activities():
    data = request.json
    location = data.get('location')
    budget = data.get('budget')
    preferences = data.get('preferences')
    activities = activity_agent.find_activities(location, preferences, budget)
    return jsonify({'activities': activities})

@app.route('/api/chatbot', methods=['POST'])
@authenticate_supabase_token
def chatbot():
    user_input = request.json.get('message')
    response = generate_chat_response(user_input)
    return jsonify({'response': response})


# Route for registering a user
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    response = register_user(email, password)
    return jsonify(response)


#  Route for logging in a user
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    response = login_user(email, password)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
