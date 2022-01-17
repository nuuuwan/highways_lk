def ccw(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return ((y3 - y1) * (x2 - x1)) > ((y2 - y1) * (x3 - x1))


def intersect(p1, p2, p3, p4):
    return (ccw(p1, p3, p4) != ccw(p2, p3, p4)) and (
        ccw(p1, p2, p3) != ccw(p1, p2, p4)
    )


# def ccw(A,B,C):
#     return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
#
# # Return true if line segments AB and CD intersect
# def intersect(A,B,C,D):
#     return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
