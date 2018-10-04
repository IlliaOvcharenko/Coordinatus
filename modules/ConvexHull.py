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


def graham(points: [Point]):
    n = len(points)
    if n <= 1:
        return points

    left_point_idx = points.index(min(points, key=lambda p: p.x))
    left_point = points.pop(left_point_idx)
    points = sorted(points, key=cmp_to_key(lambda x, y: rotate(left_point, y, x)))

    convex_hull = [left_point, points.pop(0)]
    for p in points:
        while len(convex_hull) > 1 and rotate(convex_hull[-2], convex_hull[-1], p) < 0:
            convex_hull.pop()
        convex_hull.append(p)
    return convex_hull


def jarvis(points: [Point]):
    n = len(points)
    if n <= 1:
        return points

    left_point = min(points, key=lambda p: p.x)
    points.remove(left_point)
    points.append(left_point)
    convex_hull = [left_point]

    while True:
        right = points[0]
        for p in points:
            if rotate(convex_hull[-1], right, p) < 0.0:
                right = p

        if right == left_point:
            break
        else:
            convex_hull.append(right)
            points.remove(right)

    return convex_hull


if __name__ == '__main__':
    # graham_scan([Point(1, 0), Point(10, 0), Point(0, 0)])
    # arr = [Point(1, 1), Point(2, 3), Point(4, 5)]
    # arr = sorted(arr)
    # arr.remove(Point(2, 3))
    # for i in arr:
    #     print(i)
    # print(rotate(Point(0, 0), Point(1, 0), Point(0, -1)))
    answer = graham([
        Point(0, 0),
        Point(2, 0),
        Point(0, 2),
        Point(1, 1),
        Point(2, 2)
    ])
    for p in answer:
        print(p.x, p.y)
