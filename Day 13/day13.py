#%%
TEST_MAP = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """

#%%
from typing import Set, List, Iterator, Tuple

import copy


class Cart:
    DOWN, UP, LEFT, RIGHT = "v", "^", "<", ">"
    dirdict = {
        LEFT: (-1, 0), 
        RIGHT: (1, 0),
        UP: (0, -1), 
        DOWN: (0, 1)
    }

    def __init__(self, x: int, y: int, val: str):
        self.x, self.y = x, y
        self.direction = val

        def decide():
            while (True): 
                for i in ["L", "C", "R"]: 
                    yield (i)
        
        self.decision = decide()
        self.crashed = False
    
    @property
    def position(self) -> Tuple[int, int]:
        if self.crashed:
            return False
        return self.x, self.y


    def move(self, map:"Map") -> Tuple[int, int]:
        if self.crashed:
            return (-1000,-1000)
        self.x += self.dirdict[self.direction][0]
        self.y += self.dirdict[self.direction][1]

        convert = {
                    self.DOWN: self.DOWN,
                    self.UP: self.UP,
                    self.LEFT: self.LEFT,
                    self.RIGHT: self.RIGHT
                }
        c = map.get(self.x, self.y)

        if c == "\\":
            convert = {
                self.DOWN: self.RIGHT,
                self.UP: self.LEFT,
                self.LEFT: self.UP,
                self.RIGHT: self.DOWN
            }
        elif c == "/":
            convert = {
                self.DOWN: self.LEFT,
                self.UP: self.RIGHT,
                self.LEFT: self.DOWN,
                self.RIGHT: self.UP
                }
        elif c == "+":
            decision = next(self.decision)
            if decision == "L":
                convert = {
                    self.DOWN: self.RIGHT,
                    self.UP: self.LEFT,
                    self.LEFT: self.DOWN,
                    self.RIGHT: self.UP
                }
            elif decision == "R":
                convert = {
                    self.DOWN: self.LEFT,
                    self.UP: self.RIGHT,
                    self.LEFT: self.UP,
                    self.RIGHT: self.DOWN
                }
        self.direction = convert[self.direction]

        return self.x, self.y

    def __repr__(self):
        return self.direction




class Map:

    def __init__(self, paths: str):    
        self.paths = [[c for c in p] for p in paths.splitlines()]

        self.carts = self.find_carts()

    def get(self, x: int, y: int) -> str:
        return self.paths[y][x]

    def set(self, x:int, y:int, v:str):
        self.paths[y][x] = v

    def iterate_all(self) -> Iterator[Tuple[int, int, str]]:
        for y in range(len(self.paths)):
            for x in range(len(self.paths[y])):
                yield x, y, self.get(x, y)

    def __repr__(self):
        overlay = copy.deepcopy(self.paths)
        for cart in self.carts:
            overlay[cart.y][cart.x] = str(cart)
        return "\n".join("".join(p) for p in overlay)

    def find_carts(self) -> Set[Cart]:
        carts = set()
        for x, y, v in self.iterate_all():
            if v in ["v", "^", "<", ">"]:
                carts.add(Cart(x, y, v))
                subs_dict = {
                    "v": "|",
                    "^": "|",
                    "<": "-",
                    ">": "-"
                }
                self.set(x, y, subs_dict[v])
        return carts

    def move(self, ticks:int):
        remaining = len([c for c in self.carts if not c.crashed])
        for t in range(ticks):
            for cart in self.carts:
                x, y = cart.move(self)

                if (x, y) in [c.position for c in self.carts if c is not cart]:
                    for c in [cart for cart in self.carts if cart.position == (x, y)]:
                        remaining -= 1
                        c.crashed = True
                    print(f"Crash at {x}, {y}, time {t}; {remaining} remaining carts")
                    print([c.position for c in self.carts])
                
            if remaining == 1:
                break
                                            


test_map = Map(TEST_MAP)

print(test_map)
#%%

test_map.move(100)
print(test_map)
#%%

with open("Day 13/input.txt") as f:
    txt = f.read()

map = Map(txt)
map.move(300)
#%%

new = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""

newtest_map = Map(new)
newtest_map.move(300)


#%%
map = Map(txt)
map.move(30000)

#%%
