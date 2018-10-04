"""
Point class
"""
from typing import Dict, Tuple, List


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(" + str(self.x) + " " + str(self.y) + ")"


def dict_to_points(d: [Dict[str, int]]) -> [Point]:
    return [Point(p['x'], p['y']) for p in d]


def points_to_dict(points: [Point]) -> [Dict[str, int]]:
    return [{'x': p.x, 'y': p.y} for p in points]
