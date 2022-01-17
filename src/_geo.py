def get_bbox(latlng_list):
    max_lat, max_lng = min_lat, min_lng = latlng_list[0]
    for [lat, lng] in latlng_list[1:]:
        min_lat = min(min_lat, lat)
        max_lat = max(max_lat, lat)
        min_lng = min(min_lng, lng)
        max_lng = max(max_lng, lng)
    lat_span = max_lat - min_lat
    lng_span = max_lng - min_lng

    return [
        min_lat,
        max_lat,
        min_lng,
        max_lng,
        lat_span,
        lng_span,
    ]


def get_func_transform(WIDTH, HEIGHT, PADDING, latlng_list):
    [
        min_lat,
        max_lat,
        min_lng,
        max_lng,
        lat_span,
        lng_span,
    ] = get_bbox(latlng_list)

    r = (lat_span / HEIGHT) / (lng_span / WIDTH)
    if r > 1:
        WIDTH /= r
    else:
        HEIGHT *= r

    def func_transform(latlng):
        [lat, lng] = latlng
        px = (lng - min_lng) / lng_span
        py = (lat - min_lat) / lat_span

        x = px * (WIDTH - PADDING * 2) + PADDING
        y = (1 - py) * (HEIGHT - PADDING * 2) + PADDING
        return [x, y]

    return func_transform
