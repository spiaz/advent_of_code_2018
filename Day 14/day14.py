#%%

from typing import List, Tuple
from itertools import count

elf1 = 0
elf2 = 1

scoreboard = [3, 7]

def new_recipes(elf1:int, elf2:int, scoreboard:List[int]) -> List[int]:
    combined = scoreboard[elf1] + scoreboard[elf2]
    return [int(c) for c in str(combined)]

assert new_recipes(0, 1, [3, 7]) == [1, 0]
assert new_recipes(0, 1, [3, 6]) == [9]
#%%
def move_elf(elf:int, scoreboard:List[int]) -> int:
    return (elf + scoreboard[elf] + 1) % len(scoreboard)

assert move_elf(0, [3, 7, 1, 0]) == 0
assert move_elf(1, [3, 7, 1, 0]) == 1
#%%

def move_forward(elf1:int, elf2:int, scoreboard:List[int]) -> Tuple[int, int]:
    return move_elf(elf1, scoreboard), move_elf(elf2, scoreboard)
assert move_forward(0, 1, [3, 7, 1, 0]) == (0, 1)

def ten_recipes_after_n(n_recipes:int) -> int:
    elf1 = 0
    elf2 = 1
    scoreboard = [3, 7]
    while len(scoreboard) < n_recipes + 10:
        scoreboard.extend(new_recipes(elf1, elf2, scoreboard))

        elf1, elf2 = move_forward(elf1, elf2, scoreboard)
    
    n_s = "".join(str(x) for x in scoreboard[n_recipes:n_recipes + 10])
    return int(n_s)

assert ten_recipes_after_n(9) == 5158916779
assert ten_recipes_after_n(5) == 124515891
assert ten_recipes_after_n(18) == 9251071085
assert ten_recipes_after_n(2018) == 5941429882
#%%
ten_recipes_after_n(165061)
# 5992684592

#%%

def n_recipes_before_score(score:str) -> int:
    elf1 = 0
    elf2 = 1
    scoreboard = [3, 7]

    score_l = [int(x) for x in score]
    L = len(score)

    n_recipes = 0
    
    while not n_recipes:
        recipes = new_recipes(elf1, elf2, scoreboard)
        for recipe in recipes:
            scoreboard.append(recipe)
            if score_l == scoreboard[-L:]:
                n_recipes = len(scoreboard) - L
                break
            
        elf1, elf2 = move_forward(elf1, elf2, scoreboard)
        
    return n_recipes




assert n_recipes_before_score("51589") == 9
assert n_recipes_before_score("01245") == 5
assert n_recipes_before_score("92510") == 18
assert n_recipes_before_score("59414") == 2018

#%%
n_recipes_before_score("165061")

#%%
