"""
Convex Hull algorithms
"""
from modules.Point import Point
from functools import cmp_to_key


def rotate(a: Point, b: Point, c: Point):
    """
    return positive number if point C located on the left side of the vector (a, b)
           and negative otherwise
    using z-coordinate in cross product [(a, b), (a, c)]
    """
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def graham_scan(points: [Point]):
    n = len(points)
    if n == 0:
        return []
    elif n == 1:
        return [points[0]]

    left_point_idx = points.index(min(points, key=lambda p: p.x))
    left_point = points.pop(left_point_idx)
    points = sorted(points, key=cmp_to_key(lambda x, y: rotate(left_point, y, x)))

    convex_hull = [left_point, points[0]]
    for p in points:
        while rotate(convex_hull[-2], convex_hull[-1], p) < 0 and len(convex_hull) > 1:
            convex_hull.pop()
        convex_hull.append(p)
    return convex_hull


if __name__ == '__main__':
    # build_convex_hull([Point(1, 0), Point(10, 0), Point(0, 0)])
    # arr = [Point(1, 1), Point(2, 3), Point(4, 5)]
    # arr = sorted(arr)
    # arr.remove(Point(2, 3))
    # for i in arr:
    #     print(i)
    print(rotate(Point(0, 0), Point(1, 0), Point(0, -1)))