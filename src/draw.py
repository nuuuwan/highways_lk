from utils import filex, jsonx

from __constants import (GRAPH_PLACES_FILE, GRAPH_ROADS_FILE, HEIGHT, MAP_FILE,
                         PADDING, STYLE_PLACE_CIRCLE, STYLE_PLACE_TEXT,
                         STYLE_ROAD_LINE, STYLE_ROAD_LINE_STROKE_MAP, WIDTH)
from _geo import get_func_transform
from _xmlx import _, render_xml


def get_reverse_index(xs):
    return dict(
        list(
            map(
                lambda x: [x[1], x[0]],
                enumerate(sorted(xs)),
            )
        )
    )


def transform_histogram(graph_places_index):
    lats, lngs = [], []
    for place_id, lat_lng in graph_places_index.items():
        lat, lng = lat_lng
        lats.append(lat)
        lngs.append(lng)

    print(len(lats))
    print(len(lngs))

    lats_index = get_reverse_index(lats)
    lngs_index = get_reverse_index(lngs)

    trans_graph_places_index = {}
    for place_id, lat_lng in graph_places_index.items():
        lat, lng = lat_lng
        latx, lngx = lats_index[lat], lngs_index[lng]

        trans_graph_places_index[place_id] = [latx, lngx]
    return trans_graph_places_index


def draw():

    graph_places_index = jsonx.read(GRAPH_PLACES_FILE)
    graph_places_index = transform_histogram(graph_places_index)

    latlng_list = list(graph_places_index.values())
    func_transform = get_func_transform(WIDTH, HEIGHT, PADDING, latlng_list)

    def render_place(place_item):
        place_id, lat_lng = place_item
        x, y = func_transform(lat_lng)
        return _(
            'g',
            [
                _(
                    'circle',
                    None,
                    dict(
                        cx=x,
                        cy=y,
                    )
                    | STYLE_PLACE_CIRCLE,
                ),
                _(
                    'text',
                    place_id,
                    dict(
                        x=x + STYLE_PLACE_TEXT['font_size'],
                        y=y,
                    )
                    | STYLE_PLACE_TEXT,
                ),
            ],
        )

    rendered_places = list(
        map(
            render_place,
            graph_places_index.items(),
        )
    )

    graph_roads_index = jsonx.read(GRAPH_ROADS_FILE)

    def render_road(road_item):
        road_id, places = road_item
        child_list = []
        n_places = len(places)

        for i in range(0, n_places - 1):
            place1, place2 = places[i: i + 2]
            lat_lng1 = graph_places_index[place1]
            lat_lng2 = graph_places_index[place2]
            x1, y1 = func_transform(lat_lng1)
            x2, y2 = func_transform(lat_lng2)

            child_list.append(
                _(
                    'line',
                    None,
                    dict(
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                        stroke=STYLE_ROAD_LINE_STROKE_MAP[road_id[:2]],
                    )
                    | STYLE_ROAD_LINE,
                )
            )

        return _('g', child_list)

    rendered_roads = list(
        map(
            render_road,
            graph_roads_index.items(),
        )
    )

    svg = _(
        'svg',
        rendered_roads + rendered_places,
        dict(width=WIDTH, height=HEIGHT),
    )
    filex.write(MAP_FILE, render_xml(svg))


if __name__ == '__main__':
    draw()
