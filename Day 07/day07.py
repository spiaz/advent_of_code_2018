#%%
import re

from typing import NamedTuple, Dict, List, Set, Iterator, Tuple, DefaultDict
from collections import Counter, defaultdict


class Task:
    def __init__(self):
        self.previous = 0
        self._followers = []
        self.time = 0

    @property
    def followers(self) -> List[str]:
        return self._followers

    def add_follower(self, id: str):
        self._followers.append(id)

    def __repr__(self):
        return f"{self.previous} --> {self.followers}\n"


all_tasks = List[Task]

TaskList = DefaultDict[str, Task]


def parse(lines: List[str]) -> TaskList:
    tasks: TaskList = defaultdict(Task)
    for l in lines:
        rx = re.match(
            r"Step ([A-Z]+) must be finished before step ([A-Z]+) can begin.", l.strip()
        )
        if rx:
            prev, follower = rx.groups()
            tasks[prev].add_follower(follower)
            tasks[follower].previous += 1
    return tasks


def ready_tasks(tl: TaskList) -> List[str]:
    return sorted([id for id, t in tl.items() if t.previous == 0])


def get_seq(tl: TaskList) -> str:
    seq: List[str] = []
    while ready_tasks(tl):
        t_id = ready_tasks(tl)[0]
        t = tl[t_id]
        t.previous -= 1
        for f_id in t.followers:
            f = tl[f_id]
            f.previous -= 1
        seq.append(t_id)
    return "".join(seq)


test_lines = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split(
    "\n"
)

tl = parse(test_lines)
assert ready_tasks(tl)[0] == "C"
assert len(ready_tasks(tl)) == 1

assert get_seq(tl) == "CABDFE"

#%%
with open("input.txt", "r") as target:
    lines = target.readlines()

tl = parse(lines)
get_seq(tl)

#%%


def do_task(w_time: int, tl: TaskList, t_id: str, delta=60) -> int:
    t = tl[t_id]
    task_time = ord(t_id) - ord("A") + delta + 1
    elapsed_time = max(w_time, t.time) + task_time
    t.previous -= 1
    for follower_id in t.followers:
        tl[follower_id].previous -= 1
        tl[follower_id].time = elapsed_time
    return elapsed_time


def get_time(tl: TaskList, n_workers: int, delta: int = 60) -> int:
    workers = [0] * n_workers

    while ready_tasks(tl):
        workers = sorted(workers)
        w = workers.pop(0)
        t_id = sorted(ready_tasks(tl), key=lambda t_id: tl[t_id].time)[0]
        workers.append(do_task(w, tl, t_id, delta))
    return max(workers)


tl = parse(test_lines)
get_time(tl, 2, 0)
#%%

#%%
with open("input.txt", "r") as target:
    lines = target.readlines()

tl = parse(lines)
get_time(tl, 5)

#%%
