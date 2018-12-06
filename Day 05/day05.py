#%%
from typing import List

testpol = "dabAcCaCBAcCcaDA"


def react(polymer: str) -> str:
    stack: List[str] = []
    for c in polymer:
        if len(stack) > 0 and stack[-1].lower() == c.lower() and stack[-1] != c:
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


assert react(testpol) == "dabCBAcaDA"

assert len(react(testpol)) == 10
#%%

with open("input.txt", "r") as infile:
    lines = [l.strip() for l in infile.readlines()]
input_line = lines[0]
len(react(input_line))


#%%
set(testpol.lower())


def react_with_remove(polymer: str, rm_char: str) -> int:
    stack:List[str] = []
    for c in polymer:
        if c.lower() == rm_char:
            continue
        if len(stack) > 0 and stack[-1].lower() == c.lower() and stack[-1] != c:
            stack.pop()
        else:
            stack.append(c)
    return len(stack)


assert react_with_remove(testpol, "a") == 6
assert react_with_remove(testpol, "b") == 8
assert react_with_remove(testpol, "c") == 4
assert react_with_remove(testpol, "d") == 6


def shortest_polymer(polymer: str) -> int:
    scores = []
    for c in set(polymer.lower()):
        scores.append(react_with_remove(polymer, c))
    return min(scores)


assert shortest_polymer(testpol) == 4
#%%

shortest_polymer(input_line)

#%%
