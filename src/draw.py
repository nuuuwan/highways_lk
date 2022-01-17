from utils import filex, jsonx

from __constants import (GRAPH_PLACES_FILE, GRAPH_ROADS_FILE, HEIGHT, MAP_FILE,
                         PADDING, PLACE_FILL, PLACE_RADIUS, PLACE_STROKE,
                         PLACE_STROKE_WIDTH, ROAD_FILL, ROAD_STROKE,
                         ROAD_STROKE_WIDTH, WIDTH)
from _geo import get_func_transform
from _xmlx import _, render_xml


def draw():

    graph_places_index = jsonx.read(GRAPH_PLACES_FILE)

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
                        r=PLACE_RADIUS,
                        fill=PLACE_FILL,
                        stroke=PLACE_STROKE,
                        stroke_width=PLACE_STROKE_WIDTH,
                    ),
                )
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
                        fill=ROAD_FILL,
                        stroke=ROAD_STROKE,
                        stroke_width=ROAD_STROKE_WIDTH,
                    ),
                )
            )

        return _('g', child_list)

    rendered_roads = list(
        map(
            render_road,
            graph_roads_index.items(),
        )
    )

    svg = _('svg', rendered_roads + rendered_places)
    filex.write(MAP_FILE, render_xml(svg))


if __name__ == '__main__':
    draw()
