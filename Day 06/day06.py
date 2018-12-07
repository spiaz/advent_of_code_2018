#%%

from typing import NamedTuple, List, Tuple, Counter, Iterator
import re


class Coord(NamedTuple):
    x: int
    y: int

    def distance(self, c: Coord) -> int:
        return manhattan(self, c)


class Grid(NamedTuple):
    left: int
    right: int
    top: int
    bottom: int

    def all_locations(self) -> Iterator[Coord]:
        for coord in [
            Coord(x, y)
            for y in range(self.left, self.right)
            for x in range(self.top, self.bottom)
        ]:
            yield coord

    def is_contour(self, c: Coord) -> bool:
        return c.x in [self.top, self.bottom] or c.y in [self.left, self.right]


def manhattan(a: Coord, b: Coord):
    return abs(a.x - b.x) + abs(a.y - b.y)


def build_grid(coords: List[Coord]) -> Grid:
    left = right = coords[0].y
    top = bottom = coords[0].x
    xs = [coord.x for coord in coords]
    ys = [coord.y for coord in coords]

    left = min(ys)
    right = max(ys)
    top = min(xs)
    bottom = max(xs)

    return Grid(left, right, top, bottom)


def parse_text(text: str) -> List[Coord]:
    lines = text.split("\n")
    coords = []
    id = 0
    for line in lines:
        rx = re.match(r"(\d+), (\d+)", line.strip())
        if rx:
            x, y = rx.groups()
            coords.append(Coord(int(x), int(y)))
    return coords


def closest_coord(loc: Coord, coords: List[Coord]) -> Coord:
    closest = coords[0]
    for c in coords[1:]:
        if c.distance(loc) < closest.distance(loc):
            closest = c
    return closest


def count_areas(coords: List[Coord]) -> Tuple[Coord, int]:
    grid = build_grid(coords)
    areas = Counter()
    infinite_areas = set()

    for loc in grid.all_locations():
        closest = closest_coord(loc, coords)
        areas[closest] += 1
        if grid.is_contour(loc):
            infinite_areas.add(closest)

    for c in infinite_areas:
        areas[c] = 0

    (c1, n1), (c2, n2) = areas.most_common(2)
    assert n1 > n2
    return c1, n1


TESTINPUT = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

test_coords = parse_text(TESTINPUT)

count_areas(test_coords)


#%%
with open("input.txt", "r") as target:
    coords = parse_text(target.read())
grid = build_grid(coords)

count_areas(coords)

#%%


def count_distances(coords: List[Coord], treshold: int) -> int:
    grid = build_grid(coords)
    total_distance = Counter()
    for loc in grid.all_locations():
        for coord in coords:
            total_distance[loc] += loc.distance(coord)
    values = total_distance.values()
    return len([v for v in values if v < treshold])


count_distances(test_coords, 32)

#%%
count_distances(coords, 10000)

#%%
