import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import googlemaps

GOOGLE_API_KEY = 'AIzaSyB9BjxwX1cYgLchvrmFQ5vmEsrdB46IIzM'
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

# Get public IP address to fetch current location
def get_public_ip():
    try:
        ip_response = requests.get('https://api64.ipify.org?format=json')
        ip = ip_response.json()['ip']
        return ip
    except Exception as e:
        print(f"Unable to get IP address: {e}")
        return None

# Get location by IP
def get_location_by_ip(ip):
    try:
        geo_response = requests.get(f'https://ipapi.co/{ip}/json/')
        location_data = geo_response.json()
        return location_data
    except Exception as e:
        print(f"Unable to get location data: {e}")
        return None

# Fetch user's current location (latitude, longitude)
def get_user_location():
    ip = get_public_ip()
    if ip:
        location_data = get_location_by_ip(ip)
        if location_data:
            latitude = location_data.get('latitude')
            longitude = location_data.get('longitude')
            return latitude, longitude
    else:
        print("Unable to fetch location.")
        return None

# Get autofill suggestions for a given location query
def get_location_suggestions(query):
    try:
        places_result = gmaps.places_autocomplete(query)
        return places_result
    except Exception as e:
        print(f"Unable to fetch place suggestions: {e}")
        return []

# Get location coordinates for a place
def get_place_coordinates(place_id):
    try:
        place_details = gmaps.place(place_id=place_id)
        location = place_details['result']['geometry']['location']
        return location['lat'], location['lng']
    except Exception as e:
        print(f"Unable to get place coordinates: {e}")
        return None

# Calculate distance between two coordinates
def calculate_distance(coord1, coord2, unit='miles'):
    if unit == 'miles':
        return geodesic(coord1, coord2).miles
    elif unit == 'kilometers':
        return geodesic(coord1, coord2).kilometers
    else:
        return None

# Main function to calculate distance between current location and user input
def main():
    # Get the user's current location
    user_location = get_user_location()
    
    if user_location:
        print(f"Your current location: Latitude {user_location[0]}, Longitude {user_location[1]}")

        # Get user input for destination with autofill
        query = input("Enter a destination: ")
        suggestions = get_location_suggestions(query)

        if suggestions:
            # Show the user the suggestions
            print("Here are some place suggestions:")
            for i, suggestion in enumerate(suggestions):
                print(f"{i + 1}. {suggestion['description']}")
            
            # Let the user select a place
            choice = int(input(f"Select a place by entering the corresponding number (1-{len(suggestions)}): ")) - 1
            
            # Get place coordinates for the selected place
            selected_place_id = suggestions[choice]['place_id']
            destination_coords = get_place_coordinates(selected_place_id)

            if destination_coords:
                print(f"Destination coordinates: Latitude {destination_coords[0]}, Longitude {destination_coords[1]}")
                
                # Calculate distance
                distance = calculate_distance(user_location, destination_coords, unit='miles')
                print(f"Distance from your location to the destination: {distance:.2f} miles")
            else:
                print("Unable to get destination coordinates.")
        else:
            print("No place suggestions found for the given query.")
    else:
        print("Unable to get your current location.")

# Run the main function
if __name__ == "__main__":
    main()
