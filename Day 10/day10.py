#%%
from typing import List, NamedTuple, Dict, Tuple
import numpy as np
import re


class Point(NamedTuple):
    x: int
    y: int
    vx: int
    vy: int


def parse_lines(lines: List[str]) -> List[Point]:
    points: List[Point] = []
    for line in lines:
        rx = re.match(
            "position=<\s?(-?\d+),\s+(-?\d+)> velocity=<\s?(-?\d+),\s+(-?\d+)>", line
        )
        if rx:
            points.append(Point(*[int(x) for x in rx.groups()]))
    return points


test_lines = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
""".split(
    "\n"
)

test_points = parse_lines(test_lines)
test_points
#%%


def grid_shape(points: List[Point]) -> Tuple[int, int, int, int]:
    x_max = max([point.x for point in points])
    x_min = min([point.x for point in points])
    y_max = max([point.y for point in points])
    y_min = min([point.y for point in points])

    size_x, size_y = x_max - x_min + 1, y_max - y_min + 1

    return size_x, size_y, x_min, y_min


def plot_points(points: List[Point]):
    size_x, size_y, x_min, y_min = grid_shape(points)
    grid = [["_" for _ in range(size_x)] for _ in range(size_y)]
    for point in points:
        grid[point.y - y_min][point.x - x_min] = "#"
    print("\n".join(["".join(line) for line in grid]))


def move_one(points: List[Point]) -> List[Point]:
    new_points = []
    for i, p in enumerate(points):
        x = p.x + p.vx
        y = p.y + p.vy

        new_points.append(Point(x, y, p.vx, p.vy))
    return new_points


def get_area(points = List[Point]) -> int:
    sx, sy, _, _ = grid_shape(points)
    return sx * sy

def play_sequence(points: List[Point]) -> int:
    old_area = np.inf
    old_points = points
    area = get_area(old_points)
    seconds = 0
    while area < old_area:
        seconds += 1
        old_area = area
        old_points = points
        points = move_one(old_points)
        area = get_area(points)

    plot_points(old_points)
    return seconds - 1


assert play_sequence(test_points) == 3
#%%
with open("Day 10/input.txt", "r") as f:
    lines = f.readlines()

points = parse_lines(lines)
play_sequence(points)


#%%
