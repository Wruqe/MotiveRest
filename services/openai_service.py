from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the system prompt for activity suggestions
system_prompt = (
    "You are an assistant helping a group of friends choose activities to do based on their preferences, location, and budget. "
    "Provide suggestions based on the given inputs. Be sure to consider their location and the type of activity they prefer."
)

def generate_chat_response(user_input):
    try:
        # Print the received user input to log
        print(f"Received user input: {user_input}")

        # Call the OpenAI client to create a chat completion
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input['content']}
            ]
        )

        # Extract and return the assistant's response
        chat_response = completion.choices[0].message.content
        print(f"API response: {chat_response}")
        return chat_response

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return f"Error: {str(e)}"
