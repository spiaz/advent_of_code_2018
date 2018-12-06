#%%
from typing import List, Tuple, Iterator
from collections import Counter
import re

with open("input.txt", "r") as infile:
    lines = [re.sub(r"[#@,:x]", r" ", l.strip()) for l in infile]

def parselines(lines: List[str]) -> Tuple[List[int], List[Tuple[int, int, int, int]]]:
    ids = [int(l.split()[0]) for l in lines]
    dims = [
        (int(a), int(b), int(c), int(d))
        for a, b, c, d in [l.split()[1:] for l in lines]
    ]
    return ids, dims

ids, coords = parselines(testlines)
#%%
def claim_inches(coords: List[Tuple[int, int, int, int]]) -> Iterator[Tuple[int, int]]:
    for (x_start, y_start, lrg, tall) in coords:
        for x in range(x_start, x_start + lrg):
            for y in range(y_start, y_start + tall):
                yield (x, y)

#%%
c = Counter(claim_inches(coords))

def count_overlap(lines: List[str]) -> int:
    _, coords = parselines(lines)
    c = Counter(claim_inches(coords))
    return len([d for d, cnt in c.items() if cnt > 1])

testlines = """ 1  1 3  4 4
 2   3 1  4 4
 3   5 5  2 2""".split(
    "\n"
)
assert count_overlap(testlines) == 4
#%%
print(count_overlap(lines))

#%%
def non_overlapping(lines:List[str]) -> int:
    idx, coords = parselines(lines)
    cnt = Counter(claim_inches(coords))
    for i, c in zip(idx, coords):
        inches = claim_inches([c])
        if all([cnt[x] == 1 for x in inches]):
            return i
    return -1

assert non_overlapping(testlines) == 3
non_overlapping(lines)
#%%
