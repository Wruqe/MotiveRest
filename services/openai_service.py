import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_chat_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Ensure you're using a valid model
        messages=[{"role": "user", "content": user_input}]
    )
    return response['choices'][0]['message']['content']
