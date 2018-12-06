#%%
#%%
import re
from typing import NamedTuple, List, Tuple
from datetime import datetime
from collections import Counter

TESTLINES = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""


class Note(NamedTuple):
    ts: datetime
    comment: str


class Nap(NamedTuple):
    start: datetime
    end: datetime
    id: int


def get_notes(text: str) -> List[Note]:
    notes = []
    for line in text.split("\n"):
        chunks = re.match(r"(\[.*]) (.*)", line)
        assert chunks
        ts, comment = chunks.groups()
        ts = datetime.strptime(ts, r"[%Y-%m-%d %H:%M]")
        notes.append(Note(ts, comment))
    return sorted(notes)


def get_naps(text: str) -> List[Nap]:
    notes = get_notes(text)
    naps = []

    id = None
    start_nap = None

    for ts, comment in notes:
        has_id = re.search(r"#(\d+)", comment)
        if has_id:
            assert start_nap is None
            id = int(has_id.groups()[0])
        elif "falls asleep" in comment:
            assert start_nap is None
            start_nap = ts
        elif "wakes up" in comment:
            assert start_nap is not None and id is not None
            end_nap = ts
            naps.append(Nap(start_nap, end_nap, id))
            start_nap = None
    return naps


def sleepiest_id(naps: List[Nap]) -> int:
    cnt = Counter()

    for nap in naps:
        cnt[nap.id] += nap.end.minute - nap.start.minute

    (id_1, tot_1), (id_2, tot_2) = cnt.most_common(2)
    assert tot_1 > tot_2
    return id_1


def sleepiest_minute(naps: List[Nap], id: int) -> int:
    cnt = Counter()
    for nap in naps:
        if nap.id == id:
            for m in range(nap.start.minute, nap.end.minute):
                cnt[m] += 1
    (m1, c1), (m2, c2) = cnt.most_common(2)
    assert m1 > m2
    return m1


def sleepiest_guard_x_min(text):
    naps = get_naps(text)
    guard = sleepiest_id(naps)
    return guard * sleepiest_minute(naps, guard)


assert sleepiest_guard_x_min(TESTLINES) == 240
#%%

with open("input.txt", "r") as infile:
    txt = infile.read()

print(sleepiest_guard_x_min(txt))
#%%


def overall_sleepiest_minute_x_guard(naps: List[Nap]) -> int:
    cnt = Counter()
    for nap in naps:
        for m in range(nap.start.minute, nap.end.minute):
            cnt[(m, nap.id)] += 1
    ((m1, id1), c1), (t2, c2) = cnt.most_common(2)
    assert c1 > c2
    return m1 * id1


naps = get_naps(TESTLINES)

assert overall_sleepiest_minute_x_guard(naps) == 4455


#%%
naps = get_naps(txt)
print(overall_sleepiest_minute_x_guard(naps))

#%%
