class ActivityAgent:
    def find_activities(self, location, preferences, budget):
        # Example activities for different preferences
        activities_map = {
            "outdoors": ['Hiking', 'Cycling', 'Park visit', 'Kayaking'],
            "culture": ['Museum visit', 'Art gallery', 'Historic tour'],
            "relaxation": ['Spa day', 'Beach visit', 'Coffee shop'],
            "food": ['Food tour', 'Local restaurant visit', 'Winery tour']
        }

        # Return activities based on preferences, or a default if not matched
        return activities_map.get(preferences.lower(), ["No activities found for your criteria. Please try different inputs."])
