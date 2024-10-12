class ActivityAgent:
    def find_activities(self, location, preferences, budget):
        activities_map = {
            "outdoors": ['Hiking', 'Cycling', 'Picnic in the park'],
            "culture": ['Museum visit', 'Art gallery tour', 'Historical site'],
            "relaxation": ['Spa day', 'Beach visit', 'Coffee shop'],
            "food": ['Food tour', 'Local restaurant visit', 'Winery tour']
        }

        # Initialize an empty list for found activities
        matched_activities = []

        # Loop through the list of preferences to match them
        for preference in preferences:
            # Ensure the preference is a string before calling `.lower()`
            if isinstance(preference, str):
                # Find activities based on the current preference
                activities = activities_map.get(preference.lower(), [])
                matched_activities.extend(activities)

        # If no activities are matched, return a default message
        if not matched_activities:
            return ["No activities found for your criteria. Please try different inputs."]
        
        return matched_activities
