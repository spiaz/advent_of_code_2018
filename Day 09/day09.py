#%%
line = "428 players; last marble is worth 70825 points"
test_lines = """9 players; last marble is worth 25 points
10 players; last marble is worth 1618 points
13 players; last marble is worth 7999 points
17 players; last marble is worth 1104 points
21 players; last marble is worth 6111 points
30 players; last marble is worth 5807 points""".split("\n")

test_lines_results = """high score is 32
high score is 8317
high score is 146373
high score is 2764
high score is 54718
high score is 37305""".split("\n")

import re
from typing import Tuple, List, NamedTuple
from collections import namedtuple, Counter, deque

class Game(NamedTuple):
    players:int
    max_marble:int

def parse_line(line:str) -> Game:
    regx = re.match(r"(\d+) players; last marble is worth (\d+) points", line)
    return Game(*[int(x) for x in regx.groups()])

test_games = [parse_line(l) for l in test_lines]
test_results = [int(re.match(r"high score is (\d+)", l).groups()[0]) for l in test_lines_results]
test_games
#%%

def play(game:Game) -> int:
    seq = deque([0])
    player = 0
    score = Counter()

    for marble in range(1, game.max_marble + 1):
        if marble % 23 == 0:
            score[player] += marble
            seq.rotate(7)
            score[player] += seq.pop()        
            seq.rotate(-1)
        else:
            seq.rotate(-1)
            seq.append(marble)
        
        # print(f"[{marble}] {seq}")

        player = (player + 1) % (game.players)
    return max(score.values())

assert play(Game(9, 25)) == 32
assert play(test_games[0]) == test_results[0]
#%%
[play(game) for game in test_games]
#%%
assert all([play(game) == result for game, result in zip(test_games[:5], test_results[:5])])
    
#%%
play(parse_line(line))

#%%
line2 = "428 players; last marble is worth 7082500 points"

play(parse_line(line2))

#%%
