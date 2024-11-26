from config import config
import googlemaps

gmaps = googlemaps.Client(key=config.GOOGLE_MAPS_API_KEY)

def geocode_address(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None