from flask import Flask, jsonify, request
from flask_cors import CORS
from agents.activity_agent import ActivityAgent
from services.openai_service import generate_chat_response

app = Flask(__name__)
CORS(app)

# Instantiate the activity agent
activity_agent = ActivityAgent()

@app.route('/')
def index():
    return jsonify({'message': 'Flask app is running!'})

@app.route('/api/activities', methods=['POST'])
def get_activities():
    data = request.json
    location = data.get('location')
    budget = data.get('budget')
    preferences = data.get('preferences')
    activities = activity_agent.find_activities(location, preferences, budget)
    return jsonify({'activities': activities})

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message')
    response = generate_chat_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
