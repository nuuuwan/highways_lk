import os

import googlemaps
from utils.cache import cache

CACHE_NAME, CACHE_TIMEOUT = 'highways_lk', 86400 * 365.25


def get_gmaps():
    google_api_key = os.environ['GOOGLE_API_KEY']
    gmaps = googlemaps.Client(key=google_api_key)
    return gmaps


def get_location_info(gmaps, search_text):
    @cache(CACHE_NAME, CACHE_TIMEOUT)
    def get_location_info_inner(search_text=search_text):
        print(f'gmaps.geocode({search_text})')
        return gmaps.geocode(search_text)

    geocode_results = get_location_info_inner(search_text)
    if not geocode_results:
        return None
    geocode_result = geocode_results[0]
    lat = geocode_result['geometry']['location']['lat']
    lng = geocode_result['geometry']['location']['lng']
    formatted_address = geocode_result['formatted_address']

    return [lat, lng, formatted_address]
