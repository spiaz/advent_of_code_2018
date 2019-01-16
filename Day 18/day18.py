#%%
from typing import NamedTuple, List, Dict
from enum import Enum
from copy import deepcopy
from collections import defaultdict, Counter


class Acre(Enum):
    open = "."
    trees = "|"
    lumber = "#"


class Pos(NamedTuple):
    x: int
    y: int

    def add(self, x: int, y: int) -> "Pos":
        return Pos(self.x + x, self.y + y)

    @property
    def nb8(self) -> List["Pos"]:
        return [
            self.add(x, y)
            for x, y in [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]
        ]


assert len(Pos(0, 0).nb8) == 8


class Grid(dict):
    def __init__(self, text: str = ""):
        super().__init__()
        for x, line in enumerate(text.strip().split("\n")):
            for y, val in enumerate(line):
                self[Pos(x, y)] = Acre(val)

    def __repr__(self) -> str:
        lines = []
        for x in range(len(set(p.x for p in self))):
            line = []
            for y in range(len(set(p.y for p in self))):
                line.append(self[Pos(x, y)].value)
            lines.append("".join(line))
        lines.append("")
        return "\n".join(lines)
    @property
    def total_resource_value(self) -> int:
        """
        Multiply the number of wooded acres by the number of lumberyards
        """
        c = Counter(self.__repr__())
        return c[Acre.trees.value] * c[Acre.lumber.value]

    @property
    def hash(self) -> int:
        
        return hash(frozenset(self.items()))

def minute(grid: Grid) -> Grid:
    new_grid: Grid = Grid()
    for pos in grid:
        nbs = [grid[p] for p in pos.nb8 if p in grid]

        val = grid[pos]

        # An open Acre will become filled with trees if three or more adjacent acres contained trees.
        # Otherwise, nothing happens.
        if grid[pos] == Acre.open:
            if len([p for p in nbs if p == Acre.trees]) >= 3:
                val = Acre.trees

        # An Acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards.
        # Otherwise, nothing happens.
        elif grid[pos] == Acre.trees:
            if len([p for p in nbs if p == Acre.lumber]) >= 3:
                val = Acre.lumber

        # An Acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees.
        # Otherwise, it becomes open.
        elif grid[pos] == Acre.lumber:
            if not (Acre.lumber in nbs and Acre.trees in nbs):
                val = Acre.open

        new_grid[pos] = val
    return new_grid


def evolve(grid: Grid, minutes: int = 1):
    seen = {grid.hash:0}
    i = 1
    while i <= minutes:
        
        grid = minute(grid)
        
        hash = grid.hash
        if hash in seen:
            print(hash, i, i - seen[hash], " -- Loop found :)")
            loop_len = i - seen[hash]
            
            remaining = minutes - i

            grid = evolve(grid, remaining % loop_len)
            i = minutes

        else:
            seen[hash] = i
        i += 1
    return grid


example = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""

d = Grid(example)
m1 = """
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.
"""
assert evolve(d) == Grid(m1)

m2 = """
.......#..
......|#..
.|.|||....
..##|||..#
..###|||#|
...#|||||.
|||||||||.
||||||||||
||||||||||
.|||||||||
"""
assert evolve(d, 2) == Grid(m2)

m10 = """
.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||
"""

assert evolve(d, 10) == Grid(m10)

assert evolve(d, 10).total_resource_value == 1147

with open("Day 18/input.txt") as target:
    input = target.read()

g = Grid(input)

print(evolve(g, 10).total_resource_value)

#%%
assert evolve(g, 557).hash == 1837138001941875166
assert evolve(g, 524).hash == -3254629841213156888

print(evolve(g, 1_000_000_000).total_resource_value)


#%%
