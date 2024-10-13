from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FilterService:
    def check_group_size_suitability(self, place, group_size):
        """
        Uses OpenAI API to determine if a particular group size can participate in the activities at the place.
        Declares the activity unsuitable only if it is outright impossible for the group size to participate.
        """
        try:
            # System prompt to set the role of the assistant
            system_prompt = "You are a helpful assistant that responds with clear 'yes' or 'no' answers."

            # Refine user input with place details and group size, explicitly considering solo activities
            user_input = (f"Given the following place details: "
                          f"Name: {place['name']}, "
                          f"Can a group of size {group_size} participate in the activities offered at this place? "
                          f"Only say 'no' if it is outright impossible for a group of size {group_size} to participate. "
                          f"If it is possible for the group size of {group_size} to participate in any way, respond with 'yes'.")

            # OpenAI API call using the correct method
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )

            # Extract the response from OpenAI and strip any surrounding spaces
            response_content = completion.choices[0].message.content.strip().lower()

            # Check if the response is empty or incomplete
            if not response_content:
                print(f"Empty response from OpenAI for '{place['name']}' with group size {group_size}")
                return "unknown"

            print(f"OpenAI's response for '{place['name']}' with group size {group_size}: {response_content}")
            
            # Return the OpenAI response
            return response_content

        except Exception as e:
            print(f"Error checking group size suitability: {e}")
            return "error"

    def filter_by_budget(self, places, budget):
        """
        Filters places based on the budget.
        """
        filtered_places = []
        for place in places:
            price_level = place.get('budget', 1)  # Default price_level to 1 if None
            if price_level <= budget:
                filtered_places.append(place)
            else:
                print(f"Place '{place['name']}' exceeds the budget of {budget}.")
        return filtered_places

    def filter_by_group_size(self, places, group_size):
        """
        Filters places by group size, using OpenAI's judgment for each place.
        """
        filtered_places = []
        for place in places:
            # Check if the group size is suitable for this place using OpenAI
            suitability_response = self.check_group_size_suitability(place, group_size)

            # Handle the exact response from OpenAI: 'yes' or 'no'
            if suitability_response == 'yes':
                filtered_places.append(place)
            elif suitability_response == 'no':
                print(f"Place '{place['name']}' is not suitable for group size {group_size} based on OpenAI's response.")
            elif suitability_response == 'unknown':
                print(f"OpenAI gave an empty response for '{place['name']}' with group size {group_size}. Skipping...")
            else:
                print(f"Unexpected response for '{place['name']}' with group size {group_size}: {suitability_response}")
        
        return filtered_places

    def apply_filters(self, places, budget, group_size):
        """
        Applies both budget and group size filters to the places, using OpenAI to dynamically judge group sizes.
        """
        # Apply the budget filter first
        filtered_places = self.filter_by_budget(places, budget)

        # Then apply the group size filter with OpenAI's judgment
        filtered_places = self.filter_by_group_size(filtered_places, group_size)

        return filtered_places
