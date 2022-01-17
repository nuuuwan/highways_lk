def ccw(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return (y3 - y1) * (x2 - x1) > (y2 - y2) * (x3 - x1)


def intersect(p1, p2, p3, p4):
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(
        p1, p2, p4
    )
