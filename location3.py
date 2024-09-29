import geocoder
#returns array with [long, lat]
def get_user_coordinates():    
    g = geocoder.ip('me')

    if g.ok:
        return g.latlng


import googlemaps
GOOGLE_API_KEY = 'AIzaSyB9BjxwX1cYgLchvrmFQ5vmEsrdB46IIzM'
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
from geopy.distance import geodesic

# Gets store name, address, and coordinates, returns empty array on any error
def get_store_information(query):
    # Get user input for store with autofill
    #query = input("Enter a store: ")
    try:
        suggestions = gmaps.places_autocomplete(query)
    except Exception as e:
        print(f"Unable to fetch place suggestions: {e}")
        return []

    # Show the user the suggestions
    #print("Here are some place suggestions:")
    #for i, suggestion in enumerate(suggestions):
    #    print(f"{i + 1}. {suggestion['description']}")
    # Let the user select a place
    #choice = int(input(f"Select a place by entering the corresponding number (1-{len(suggestions)}): ")) - 1
    selected_place_id = suggestions[0]['place_id']

    # Get place coordinates for the selected place (default to first option)
    try:
        place_details = gmaps.place(place_id=selected_place_id)
        name = place_details['result']['name']
        address = place_details['result']['formatted_address']  # Get the full address (optional)
        location = place_details['result']['geometry']['location']
        coordinates = [location['lat'], location['lng']]
    except Exception as e:
        print(f"Unable to get place coordinates: {e}")
        return None    

    return name, address, coordinates

def calculate_miles(user_coordinates, store_coordinates):
   return geodesic(user_coordinates, store_coordinates).miles

def calculate_drive_time(user_coordinates, store_coordinates):
    directions = gmaps.directions(user_coordinates, store_coordinates, mode="driving")
    driving_time = directions[0]['legs'][0]['duration']['text']
    return driving_time


#user_coordinates = get_user_coordinates()
#print(f"Current location: Latitude {user_coordinates[0]}, Longitude {user_coordinates[1]}")

#store_name, store_address, store_coordinates = get_store_information()
#print(f"Store name: {store_name}")
#print(f"Address: {store_address}")
#print(f"Store coordinates: Latitude {store_coordinates[0]}, Longitude {store_coordinates[1]}")

#distance = calculate_miles(user_coordinates, store_coordinates)
#print(f"Distance from your location to the destination: {distance:.2f} miles")

#drive_time = calculate_drive_time(user_coordinates, store_coordinates)
#print(f"Drive time: {drive_time}")