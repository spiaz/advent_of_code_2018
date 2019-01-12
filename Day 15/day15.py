#%%

from typing import NamedTuple, List, Set, Deque
from collections import namedtuple, deque
from dataclasses import dataclass, field
import enum


class Position(NamedTuple):
    x: int
    y: int

    def add(self, p: "Position") -> "Position":
        return Position(self.x + p.x, self.y + p.y)

    @property
    def adjacents(self) -> List["Position"]:
        return sorted(
            [
                self.add(p)
                for p in [
                    Position(0, 1),
                    Position(0, -1),
                    Position(1, 0),
                    Position(-1, 0),
                ]
            ]
        )


p = Position(1, 1)
assert p.adjacents == sorted(
    [Position(1, 2), Position(1, 0), Position(2, 1), Position(0, 1)]
)


class Team(enum.Enum):
    Elf = enum.auto()
    Goblin = enum.auto()


@dataclass
class Unit:
    pos: Position
    team: Team
    hp: int = 200
    attack_power: int = 3
    is_alive: bool = True

    def attack(self, unit: "Unit"):
        unit.hp -= self.attack_power
        if unit.hp < 0:
            unit.is_alive = False

class Map:
    def __init__(self, text: str):
        lines = text.strip().split("\n")
        self.walls: Set[Position] = set()
        self.all_units: List[Unit] = []
        for x, line in enumerate(lines):
            for y, el in enumerate(line):
                if el == "#":
                    self.walls.add(Position(x, y))
                elif el in "EG":
                    team = {"E": Team.Elf, "G": Team.Goblin}[el]
                    self.all_units.append(Unit(Position(x, y), team))
        print(self)

    @property
    def units(self) -> List[Unit]:
        return sorted([u for u in self.all_units if u.is_alive], key=lambda x: x.pos)

    def __repr__(self) -> str:
        s = []
        for x in range(max(self.walls).x + 1):
            line = []
            for y in range(max(self.walls).y + 1):
                p = Position(x, y)
                if p in self.walls:
                    line.append("#")
                elif p in [u.pos for u in self.units]:
                    team = [u.team for u in self.units if u.pos == p][0]
                    line.append({Team.Elf: "E", Team.Goblin: "G"}[team])
                else:
                    line.append(".")
            s.append("".join(line))
        return "\n".join(s)

    def round(self) -> bool:
        # Quit if no enemies are alive
        if not [u for u in self.units if u.team != self.units[0].team]:
            return False

        for unit in self.units:
            if not unit.is_alive:
                continue
            enemies = [u for u in self.units if u.team != unit.team]

            if not enemies:
                return False

            in_range = set(p for e in enemies for p in e.pos.adjacents)

            # if enemy not in range, move
            if unit.pos not in in_range:
                self.move(unit)

            # if enemy in range, attack
            if unit.pos in in_range:
                chosen = min([e for e in enemies if e.pos in unit.pos.adjacents], key=lambda u: (u.hp, u.pos))
                unit.attack(chosen)
        return True


    def move(self, unit: Unit):
        enemies = [u for u in self.units if u.team != unit.team]
        obstacles = self.walls | set(u.pos for u in self.units)

        in_range = set(
            p for e in enemies for p in e.pos.adjacents if p not in obstacles
        )
 
        paths = deque((1, p, p) for p in unit.pos.adjacents if p not in obstacles)

        visited: Set[Position] = set(p for p in unit.pos.adjacents)
        visited.add(unit.pos)

        while paths:
            dist, end, start = paths.popleft()

            if end in in_range:
                paths.append((dist, end, start))
                break

            for a in end.adjacents:
                if a in obstacles or a in visited:
                    continue

                paths.append((dist + 1, a, start))
                visited.add(a)
        
        if paths:
            _, _, start = sorted(paths)[0]
            unit.pos = start
        
    def all_rounds(self):
        i = 0

        while self.round():
            i += 1
            print("Round ", i)
        return i * sum([u.hp for u in self.units])


map3 = """
#######   
#.G...#  
#...EG#  
#.#.#G#  
#..G#E#  
#.....#   
#######
"""

map = Map(map3)

assert map.all_rounds() == 27730

map4 = """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
"""
map = Map(map4)

assert map.all_rounds() == 36334


#%%
map5 = """
####### 
#E..EG# 
#.#G.E# 
#E.##E# 
#G..#.# 
#..E#.# 
#######
"""
map = Map(map5)
assert map.all_rounds() == 39514


#%%
map6 = """
#######  
#E.G#.#  
#.#G..#  
#G.#.G#  
#G..#.#  
#...E.#  
#######  
"""
map = Map(map6)
assert map.all_rounds() == 27755
#%%

with open("Day 15/input.txt") as target:

    a_map = target.read()

map = Map(a_map) # 255570
map.all_rounds()

#%%
