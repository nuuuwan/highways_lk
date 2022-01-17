URL_RAW = 'http://www.rda.gov.lk/source/rda_roads.htm'
RAW_HTML_FILE = 'data/raw.html'
ROADS_FILE = 'data/roads.tsv'
GRAPH_PLACES_FILE = 'data/graph.places.json'
GRAPH_ROADS_FILE = 'data/graph.roads.json'
MAP_FILE = 'data/map.svg'


STYLE_PLACE_CIRCLE = dict(
    r=6,
    fill='white',
    stroke='gray',
    stroke_width=3,
)

STYLE_PLACE_TEXT = dict(
    fill='black',
    stroke='none',
    font_size=9,
    text_anchor='start',
)

STYLE_ROAD_LINE = dict(
    fill='none',
    stroke_width=3,
)

STYLE_ROAD_LINE_STROKE_MAP = dict(
    AA='red',
    E0='purple',
)


WIDTH = 1200
HEIGHT = WIDTH
PADDING = 50
