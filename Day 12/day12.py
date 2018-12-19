#%%
TEST = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""".split(
    "\n"
)

from typing import List, Dict, Tuple, DefaultDict, NamedTuple
from collections import defaultdict, deque
import re


class Notes(DefaultDict):
    def __missing__(self, key):
        return "."


class Generation(NamedTuple):
    state: str
    zero: int


def parse_lines(lines: List[str]) -> Tuple[str, Notes]:
    inirx = re.match("initial state: ([\.#]+)", lines[0])
    assert inirx
    notes = Notes()
    initial_state = inirx.groups()[0]
    for line in lines[2:]:
        rx = re.match("([\.#]+) => ([\.#])", line)
        if rx:
            state, result = rx.groups()

            notes[state] = result
    # assert "....." not in notes.keys()
    return initial_state, notes


test_initial_state, test_notes = parse_lines(TEST)

with open("Day 12/input.txt", "r") as f:
    lines = f.readlines()
initial_state, notes = parse_lines(lines)
#%%


def forward_generations(state: str, notes: Notes, generations: int) -> Tuple[str, int]:
    i_zero = 0

    for gen in range(generations):
        if not gen + 1 % 1000:
            print(gen)
        new_state = ""
        # padding
        if "#" in state[:4]:
            state = "...." + state
            i_zero += 4
        if "#" in state[-4:]:
            state = state + "...."
        for code in [state[i - 2 : i + 3] for i in range(2, len(state) - 2)]:
            new_state += notes[code]
        state = new_state
        # 2 pads are always lost on the left
        i_zero -= 2
    return "".join(new_state), i_zero


print(test_initial_state)
forward_generations(test_initial_state, test_notes, 20)


#%%
test_results = {
    1: "...#...#....#.....#..#..#..#...........",
    2: "...##..##...##....#..#..#..##..........",
    3: "..#.#...#..#.#....#..#..#...#..........",
    4: "...#.#..#...#.#...#..#..##..##.........",
    5: "....#...##...#.#..#..#...#...#.........",
    6: "....##.#.#....#...#..##..##..##........",
    7: "...#..###.#...##..#...#...#...#........",
    8: "...#....##.#.#.#..##..##..##..##.......",
    9: "...##..#..#####....#...#...#...#.......",
    10: "..#.#..#...#.##....##..##..##..##......",
    11: "...#...##...#.#...#.#...#...#...#......",
    12: "...##.#.#....#.#...#.#..##..##..##.....",
    13: "..#..###.#....#.#...#....#...#...#.....",
    14: "..#....##.#....#.#..##...##..##..##....",
    15: "..##..#..#.#....#....#..#.#...#...#....",
    16: ".#.#..#...#.#...##...#...#.#..##..##...",
    17: "..#...##...#.#.#.#...##...#....#...#...",
    18: "..##.#.#....#####.#.#.#...##...##..##..",
    19: ".#..###.#..#.#.#######.#.#.#..#.#...#..",
    20: ".#....##....#####...#######....#.#..##.",
}


def pad_cut(gen: Generation, L: int = 39) -> str:
    state, i_zero = gen
    state = "..." + state + "".join(["."] * L)
    i_zero += 3
    start = i_zero - 3
    stop = start + L
    return state[start:stop]


def crop(state: str, i_zero: int = 0) -> Tuple[str, int]:
    vals = [i for i, v in enumerate(state) if v == "#"]
    m = min(vals)
    M = max(vals)
    return state[m : M + 1], i_zero - m


for i in range(1, 21):
    state, i_zero = forward_generations(test_initial_state, test_notes, i)
    state, i_zero = crop(state, i_zero)
    assert state == crop(test_results[i])[0]
#%%
def count(state: str, zero: int) -> int:
    return sum(i - zero for i, v in enumerate(state) if v == "#")


state, i_zero = forward_generations(test_initial_state, test_notes, 20)
assert count(state, i_zero) == 325
#%%

state, i_zero = forward_generations(initial_state, notes, 20)
count(state, i_zero)

#%%


def search_loop(
    state: str, notes: Notes, end_time: int
) -> Tuple[bool, str, int, int, int]:
    state, i_zero = crop(state, 0)

    states: Dict[str, Tuple[int, int]] = {}
    time = 0

    has_loop = False

    while time < end_time:
        time += 1
        # padding
        state = "...." + state + "...."
        i_zero += 2
        state = "".join(
            [
                notes[code]
                for code in [state[i - 2 : i + 3] for i in range(2, len(state) - 2)]
            ]
        )

        state, i_zero = crop(state, i_zero)

        if state in states:
            loop_len = time - states[state][0]
            i_delta = i_zero - states[state][1]
            print(f"found a loop of len {loop_len} and i_delta of {i_delta}")
            has_loop = True
            break
        else:
            states[state] = (time, i_zero)
    return has_loop, state, i_zero, i_delta, time


#%%

has_loop, state, i_zero, i_delta, time = search_loop(
    initial_state, notes, 50_000_000_000
)

if has_loop:
    delta_t = 50_000_000_000 - time
    i_zero += i_delta * delta_t
    print(count(state, i_zero))

