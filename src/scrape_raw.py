import re

from bs4 import BeautifulSoup
from utils import ds, jsonx, tsv, www

from _gmaps import get_gmaps, get_location_info

URL_RAW = 'http://www.rda.gov.lk/source/rda_roads.htm'
RAW_HTML_FILE = 'data/raw.html'
ROADS_FILE = 'data/roads.tsv'
GRAPH_PLACES_FILE = 'data/graph.places.json'
GRAPH_ROADS_FILE = 'data/graph.roads.json'


def download_raw():
    www.download_binary(URL_RAW, RAW_HTML_FILE)


def parse_raw():

    with open(RAW_HTML_FILE, 'rb') as fin:
        html = fin.read()
        fin.close()

    soup = BeautifulSoup(html, 'html.parser')
    roads_index = {}
    for table in soup.find_all('table'):
        for tr in table.find_all('tr'):
            td_text_list = list(
                map(
                    lambda td: td.text,
                    tr.find_all('td'),
                )
            )
            if len(td_text_list) != 3:
                continue
            if td_text_list[0] == '':
                continue
            road_id, desc, length_str = td_text_list
            length = (float)(length_str)
            roads_index[road_id] = dict(
                road_id=road_id,
                desc=desc,
                length=length,
            )

    roads = sorted(
        list(roads_index.values()),
        key=lambda d: d['road_id'],
    )
    tsv.write(ROADS_FILE, roads)


def add_latlng(gmaps, place):
    [lat, lng, formatted_address] = get_location_info(gmaps, place['place_id'])
    print([lat, lng, formatted_address])
    place['lat_lng'] = [lat, lng]
    place['address'] = formatted_address
    return place


def build_graph(gmaps):
    roads = tsv.read(ROADS_FILE)
    graph_roads_index = {}
    locations_all = []
    for road in roads:
        locations = list(
            map(
                lambda location: re.sub(r'\s+', ' ', location.strip()),
                road['desc'].split(' - '),
            )
        )
        locations_all += locations
        graph_roads_index[road['road_id']] = dict(locations=locations)

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
    # download_raw()
    # parse_raw()
    gmaps = get_gmaps()
    build_graph(gmaps)
