#%%
import re
from typing import NamedTuple, Set, List, Optional, Dict, Tuple
from dataclasses import dataclass
from collections import deque
from enum import Enum, auto

test_scan = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""


class Limits(NamedTuple):
    up: int
    down: int
    left: int
    right: int


class Position(NamedTuple):
    x: int
    y: int

    def add(self, x: int, y: int) -> "Position":
        return Position(self.x + x, self.y + y)

    @property
    def up(self) -> "Position":
        return self.add(0, -1)

    @property
    def left(self) -> "Position":
        return self.add(-1, 0)

    @property
    def right(self) -> "Position":
        return self.add(1, 0)

    @property
    def down(self) -> "Position":
        return self.add(0, 1)


class Material(Enum):
    clay = "#"
    water = "W"
    flowing = "F"


class Grid(dict):
    def __init__(self, clays: Set[Position], spring: Position):
        super().__init__()
        self.spring = spring

        for c in clays:
            self[c] = Material.clay

        self.limits = Limits(
            min([y for _, y in self.keys()]),
            max([y for _, y in self.keys()]),
            min([x for x, _ in self.keys()]),
            max([x for x, _ in self.keys()]),
        )

    def __repr__(self) -> str:
        s = []
        for y in range(self.limits.up, self.limits.down + 1):
            line = []
            for x in range(self.limits.left, self.limits.right + 1):
                xy = Position(x, y)
                if xy in self.keys():
                    line.append(self[xy].value)
                else:
                    line.append(".")
            s.append("".join(line) + f" {y}")
        return "\n".join(s)


def parse_scan(scan: str, spring: Optional[Position] = None) -> Grid:

    if not spring:
        spring = Position(500, 0)

    clays: Set[Position] = set()

    for line in scan.strip().split("\n"):
        x_part, y_part = line.split(", ")

        if "x" in y_part:
            x_part, y_part = y_part, x_part

        def parse(num: str) -> List[int]:
            nums = re.findall(r"(\d+)", num)
            n = [int(n) for n in nums]
            if len(n) > 1:
                n = list(range(n[0], n[1] + 1))
            return n

        x_parsed, y_parsed = parse(x_part), parse(y_part)

        clays |= set(Position(x, y) for x in x_parsed for y in y_parsed)

    return Grid(clays, spring)


def fill(grid: Grid) -> Tuple[int, int]:
    pos = Position(grid.spring.x, grid.limits.up)
    frontier = [pos]

    grid[pos] = Material.water
    i = 0
    while frontier:
        pos = frontier.pop()
        i += 1

        # down not observed
        if pos.down not in grid:
            # down is border
            if pos.down.y > grid.limits.down:
                grid[pos] = Material.flowing
            # explore down
            else:
                grid[pos.down] = Material.water
                frontier.append(pos)
                frontier.append(pos.down)
        # over something
        else:
            # over flowing water
            if grid[pos.down] == Material.flowing:
                grid[pos] = Material.flowing
                # propagate laterally
                if pos.left in grid and grid[pos.left] == Material.water:
                    grid[pos.left] = Material.flowing
                    frontier.append(pos.left)
                if pos.right in grid and grid[pos.right] == Material.water:
                    grid[pos.right] = Material.flowing
                    frontier.append(pos.right)
            # is flowing but not over flowing water: expand laterally
            elif grid[pos] == Material.flowing:
                if pos.right not in grid or grid[pos.right] == Material.water:
                    grid[pos.right] = Material.flowing
                    frontier.append(pos.right)
                if pos.left not in grid or grid[pos.left] == Material.water:
                    grid[pos.left] = Material.flowing
                    frontier.append(pos.left)
            # Not flowing
            else:
                if pos.down in grid and grid[pos.down] != Material.flowing and pos.left not in grid:
                    grid[pos.left] = Material.water
                    frontier.append(pos.left)
                
                if pos.right not in grid:
                    grid[pos.right] = Material.water
                    frontier.append(pos.right)
                
                if Material.flowing in [grid[pos.left], grid[pos.right]]:
                    grid[pos] = Material.flowing
    all = len([p for p, v in grid.items() if v in (Material.water, Material.flowing)])
    retained = len([p for p, v in grid.items() if v == Material.water])
    return all, retained

grid = parse_scan(test_scan)
print(grid)
assert fill(grid) == (57, 29)

#%%

with open("Day 17/input.txt") as target:
    lines = target.read()

grid = parse_scan(lines)
print(fill(grid))
#%%
