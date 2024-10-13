import googlemaps
import os

class GoogleMapsService:

    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.client = googlemaps.Client(self.api_key)

    def search_nearby(self, location, activity_type):
        """
        Fetch places based on location and activity type from Google Maps API.
        """
        response = self.client.places_nearby(
            location=location,
            radius=5000,  # Customize the radius if needed
            type=activity_type  # Filter by type (e.g., restaurant, park, etc.)
        )
        return response.get('results', [])
