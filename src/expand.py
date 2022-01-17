import re

from utils import ds, jsonx, tsv

from __constants import GRAPH_PLACES_FILE, GRAPH_ROADS_FILE, ROADS_FILE
from _gmaps import get_gmaps, get_location_info
from _trig import intersect
from data.CUSTOM_PLACE_LAT_LNG import CUSTOM_PLACE_LAT_LNG
from data.CUSTOM_ROAD_OVERRIDE import CUSTOM_ROAD_OVERRIDE


def round_x(x):
    return round(x, 6)


def analyze_intersections():
    graph_places_index, graph_roads_index = jsonx.read(
        GRAPH_PLACES_FILE
    ), jsonx.read(GRAPH_ROADS_FILE)

    for road_id1 in graph_roads_index:
        places1 = graph_roads_index[road_id1]
        n_places1 = len(places1)

        for road_id2 in graph_roads_index:
            if road_id2 == road_id1:
                continue
            places2 = graph_roads_index[road_id2]
            n_places2 = len(places2)

            for i1 in range(0, n_places1 - 1):
                place11, place12 = places1[i1: i1 + 2]

                p11, p12 = (
                    graph_places_index[place11],
                    graph_places_index[place12],
                )

                for i2 in range(0, n_places2 - 1):
                    place21, place22 = places2[i2: i2 + 2]

                    if place21 in [place11, place12] or place22 in [
                        place11,
                        place12,
                    ]:
                        continue

                    p21, p22 = (
                        graph_places_index[place21],
                        graph_places_index[place22],
                    )

                    if intersect(p11, p12, p21, p22):
                        f'{road_id1}x{road_id2}'

                        print(
                            f'{place11} -> {place12} ({road_id1})',
                            f' x {place21} -> {place22} ({road_id2})',
                        )


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

    return [round_x(lat), round_x(lng)]


def build_graph(gmaps):
    roads = tsv.read(ROADS_FILE)
    graph_roads_index = {}
    for road in roads:
        if 'AA0' != road['road_id'][:3] and 'E00' != road['road_id'][:3]:
            continue
        locations = list(
            map(
                lambda location: re.sub(r'\s+', ' ', location.strip()),
                road['desc'].split(' - '),
            )
        )
        graph_roads_index[road['road_id']] = locations

    for k, v in CUSTOM_ROAD_OVERRIDE.items():
        graph_roads_index[k] = v

    locations_all = []
    for k, v in graph_roads_index.items():
        locations_all += v
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
        GRAPH_ROADS_FILE,
        graph_roads_index,
    )
    jsonx.write(
        GRAPH_PLACES_FILE,
        graph_places_index,
    )


if __name__ == '__main__':
    gmaps = get_gmaps()
    build_graph(gmaps)
    print('...')
    analyze_intersections()
