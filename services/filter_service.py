class FilterService:

    def filter_by_budget(self, places, budget):
        filtered_places = []
        for place in places:
            if place.get('price_level', 0) <= budget:
                filtered_places.append(place)
            else:
                print(f"Place '{place['name']}' exceeds the budget of {budget}.")
        return filtered_places

    def filter_by_group_size(self, places, group_size):
        group_tag_map = {
            1: 'solo_friendly',
            2: ['solo_friendly', 'couple_friendly'],  # Allow both solo and couple-friendly places for a group of 2
            3: 'small_group_friendly',
            4: 'large_group_friendly'
        }
        group_tags = group_tag_map.get(group_size, 'large_group_friendly')

        filtered_places = []
        for place in places:
            tags = place.get('tags', [])
            print(f"Checking place '{place['name']}' with tags: {tags} for group size {group_size} (looking for {group_tags}).")
            
            # Check if any of the acceptable tags for the group size are in the place's tags
            if isinstance(group_tags, list):  # If it's a list of acceptable tags
                if any(tag in tags for tag in group_tags):
                    filtered_places.append(place)
                else:
                    print(f"Place '{place['name']}' does not match any of the group size tags: {group_tags}.")
            else:  # If it's a single tag
                if group_tags in tags:
                    filtered_places.append(place)
                else:
                    print(f"Place '{place['name']}' does not match the group size tag '{group_tags}'.")

        return filtered_places

    def apply_filters(self, places, budget, group_size):
        """
        Applies both budget and group size filters to the places.
        """
        # Apply the budget filter first
        filtered_places = self.filter_by_budget(places, budget)

        # Then apply the group size filter
        filtered_places = self.filter_by_group_size(filtered_places, group_size)

        return filtered_places
