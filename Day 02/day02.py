#%%
from collections import Counter
from typing import List, Iterator

with open("input.txt", "r") as target:
    codes = [l.strip() for l in target]

def count_codes(codes:List) -> int:
    twos, threes = 0, 0
    for c in codes:
        chk = Counter(c)
        if 2 in chk.values():
            twos += 1
        if 3 in chk.values():
            threes += 1
    return twos * threes

assert count_codes(["abcdef",
"bababc",
"abbcde",
"abcccd",
"aabcdd",
"abcdee",
"ababab",]) == 12

count_codes(codes)

#%%
def generate_sequences(codes:List[str]) -> Iterator[str]:
    for c in codes:
        for i in range(len(c)):
            seq = c[:i] + "_" + c[i+1:]
            yield(seq) 

def find_one_char_distance(codes:List[str]) -> str:
    chk = Counter(generate_sequences(codes))
    assert max(chk.values()) == 2
    assert min(chk.values()) == 1

    k, _ = chk.most_common(1)[0]
    return  "".join(k.split("_"))

find_one_char_distance(codes)


#%%
