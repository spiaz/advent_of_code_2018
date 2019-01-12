#%%
import re
from typing import NamedTuple, Dict, Tuple, Set, List
from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from collections import Counter


class Register(NamedTuple):
    a: int
    b: int
    c: int
    d: int


class Instruction(NamedTuple):
    code: int
    a: int
    b: int
    c: int


class Sample(NamedTuple):
    before: Register
    instr: Instruction
    after: Register


def addr(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = r[i.a] + r[i.b]
    return Register(*vals)


def addi(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = r[i.a] + i.b
    return Register(*vals)


def mulr(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = r[i.a] * r[i.b]
    return Register(*vals)


def muli(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = r[i.a] * i.b
    return Register(*vals)


def banr(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = r[i.a] & r[i.b]
    return Register(*vals)


def bani(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = r[i.a] & i.b
    return Register(*vals)


def borr(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = r[i.a] | r[i.b]
    return Register(*vals)


def bori(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = r[i.a] | i.b
    return Register(*vals)


def setr(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = r[i.a]
    return Register(*vals)


def seti(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = i.a
    return Register(*vals)


def gtir(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = 1 if i.a > r[i.b] else 0
    return Register(*vals)


def gtri(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = 1 if r[i.a] > i.b else 0
    return Register(*vals)


def gtrr(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = 1 if r[i.a] > r[i.b] else 0
    return Register(*vals)


def eqir(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = 1 if i.a == r[i.b] else 0
    return Register(*vals)


def eqri(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = 1 if r[i.a] == i.b else 0
    return Register(*vals)


def eqrr(r: Register, i=Instruction) -> Register:
    vals = list(r)
    vals[i.c] = 1 if r[i.a] == r[i.b] else 0
    return Register(*vals)


operations = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}


def more_than_3(s: Sample) -> bool:
    cnt = 0

    for op in operations.values():
        if op(s.before, s.instr) == s.after:
            cnt += 1
            if cnt >= 3:
                return True
    return False


def cnt_more_than_3(samples: List[Sample]) -> int:
    cnt = 0
    for sample in samples:
        if more_than_3(sample):
            cnt += 1
    return cnt


def read_samples(text: str) -> List[Sample]:
    items = text.split("\n\n")
    samples = []
    for item in items:
        values = re.findall(r"(\d+)", item)

        v = [int(v) for v in values]

        before = Register(*v[:4])
        instruction = Instruction(*v[4:8])
        after = Register(*v[8:])
        samples.append(Sample(before, instruction, after))

    return samples


#%%
text = """before = Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]"""

samples = read_samples(text)

assert cnt_more_than_3(samples) == 1

#%%
with open("Day 16/input.txt", "r") as target:
    input = target.read()

text, test_program = input.split("\n\n\n")

samples = read_samples(text)
cnt_more_than_3(samples)
#%%

op_to_code = {o: set(range(16)) for o in operations}


def validate(sample: Sample, op_to_code: Dict) -> Dict:
    valid = set(op for op in op_to_code if sample.instr.code in op_to_code[op])
    if valid:
        for op in valid:
            if operations[op](sample.before, sample.instr) != sample.after:
                op_to_code[op].remove(sample.instr.code)
    return op_to_code


def consolidate(d: Dict) -> Dict:
    c = Counter([k for k, v in d.items() for x in v])

    assigned = {}
    while 1 in c.values():
        k, cnt = c.most_common()[-1]
        assert cnt == 1
        val = d[k].pop()
        assigned[k] = val

        for k in d:
            d[k] = [v for v in d[k] if v != val]
        c = Counter([k for k, v in d.items() for x in v])

    return assigned


for sample in samples:
    op_to_code = validate(sample, op_to_code)

op_to_code = consolidate(op_to_code)

code_to_op = {v: k for k, v in op_to_code.items()}
#%%

test_program
instr = []
for line in test_program.strip().split("\n"):
    rx = re.match(r"(\d+) (\d+) (\d+) (\d+)", line)
    instr.append(Instruction(*[int(x) for x in rx.groups()]))
#%%
code_to_op
#%%
r = Register(0, 0, 0, 0)

for i in instr:
    r = operations[code_to_op[i.code]](r, i)
r   
