import re

from utils import ds, jsonx, tsv

from __constants import GRAPH_PLACES_FILE, GRAPH_ROADS_FILE, ROADS_FILE
from _gmaps import get_gmaps, get_location_info
from data.CUSTOM_PLACE_LAT_LNG import CUSTOM_PLACE_LAT_LNG
from data.CUSTOM_ROAD_OVERRIDE import CUSTOM_ROAD_OVERRIDE


def round_x(x):
    return round(x, 6)


def add_latlng(gmaps, place):
    place_id = place['place_id']

    if place_id in CUSTOM_PLACE_LAT_LNG:
        lat, lng = CUSTOM_PLACE_LAT_LNG[place_id]
    else:
        search_text = place_id + ', Sri Lanka'
        result = get_location_info(gmaps, search_text)
        if result is None:
            return []

        [lat, lng, formatted_address] = result
        print([lat, lng, formatted_address])

    return [round_x(lat), round_x(lng)]


def build_graph(gmaps):
    roads = tsv.read(ROADS_FILE)
    graph_roads_index = {}
    locations_all = []
    for road in roads:
        if 'AA' not in road['road_id']:
            continue
        locations = list(
            map(
                lambda location: re.sub(r'\s+', ' ', location.strip()),
                road['desc'].split(' - '),
            )
        )
        locations_all += locations
        graph_roads_index[road['road_id']] = locations

    for k, v in CUSTOM_ROAD_OVERRIDE.items():
        graph_roads_index[k] = v

    jsonx.write(
        GRAPH_ROADS_FILE,
        graph_roads_index,
    )

    locations_all = sorted(ds.unique(locations_all))

    graph_places_index = dict(
        list(
            map(
                lambda location: [location, dict(place_id=location)],
                locations_all,
            )
        )
    )

    graph_places_index = dict(
        list(
            map(
                lambda x: [x[0], add_latlng(gmaps, x[1])],
                graph_places_index.items(),
            )
        )
    )

    jsonx.write(
        GRAPH_PLACES_FILE,
        graph_places_index,
    )


if __name__ == '__main__':
    gmaps = get_gmaps()
    build_graph(gmaps)
