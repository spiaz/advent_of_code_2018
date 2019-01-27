#%%
from typing import List, NamedTuple, Optional
import dataclasses
import re


class Instruction(NamedTuple):
    code: str
    A: int
    B: int
    C: int


def execute(r: List[int], instr: Instruction) -> List[int]:
    code, A, B, C = instr

    if code == "addr":
        # addr (add register) stores into register C the result of adding register A and register B.
        r[C] = r[A] + r[B]
    elif code == "addi":
        # addi (add immediate) stores into register C the result of adding register A and value B.
        r[C] = r[A] + B
    elif code == "mulr":
        # mulr (multiply register) stores into register C the result of multiplying register A and register B.
        r[C] = r[A] * r[B]
    elif code == "muli":
        # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
        r[C] = r[A] * B
    elif code == "banr":
        # banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
        r[C] = r[A] & r[B]
    elif code == "bani":
        # bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
        r[C] = r[A] & B
    elif code == "borr":
        # borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
        r[C] = r[A] | r[B]
    elif code == "bori":
        # bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
        r[C] = r[A] | B
    elif code == "setr":
        # setr (set register) copies the contents of register A into register C. (Input B is ignored.)
        r[C] = r[A]
    elif code == "seti":
        # seti (set immediate) stores value A into register C. (Input B is ignored.)
        r[C] = A
    elif code == "gtir":
        # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        r[C] = 1 if A > r[B] else 0
    elif code == "gtri":
        # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        r[C] = 1 if r[A] > B else 0
    elif code == "gtrr":
        # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        r[C] = 1 if r[A] > r[B] else 0
    elif code == "eqir":
        # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        r[C] = 1 if A == r[B] else 0
    elif code == "eqri":
        # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        r[C] = 1 if r[A] == B else 0
    elif code == "eqrr":
        # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        r[C] = 1 if r[A] == r[B] else 0
    return r


RE_IP_BOUND = re.compile(r"#ip (\d)")


def run_program(program: str, registers: Optional[List[int]] = None) -> List[int]:
    if registers is None:
        registers = [0, 0, 0, 0, 0, 0]
    ip = 0
    ip_reg = None
    lines = program.strip().split("\n")

    r0 = None

    while True:
        try:
            if registers[0] != r0:
                r0 = registers[0]
                print(r0)

            line = lines[ip]

            ip_bound = re.match(RE_IP_BOUND, line)
            if ip_bound:
                # bound ip and register 
                ip_reg = int(ip_bound.groups()[0])
                ip = registers[ip_reg]
                lines.pop(ip)

            else:
                print(ip, registers)
                el = line.split(" ")

                if ip_reg is not None:
                    # When the instruction pointer is bound to a register,
                    # its value is written to that register
                    registers[ip_reg] = ip

                instr = Instruction(el[0], int(el[1]), int(el[2]), int(el[3]))
                registers = execute(registers, instr)

                if ip_reg is not None:
                    # the value of that register is written back to the 
                    # instruction pointer immediately after each instruction
                    ip = registers[ip_reg]
                ip += 1
        except IndexError:
            break

    return registers


test_input = """
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

# What value is left in register 0 when the background process halts?
registers = run_program(test_input)
assert registers[0] == 6
#%%
with open("Day 19/input.txt", "r") as infile:
    program = infile.read()

registers = run_program(program)
print(registers[0])

#%% PART 2
with open("Day 19/input.txt", "r") as infile:
    program = infile.read()

registers = run_program(program, registers=[1, 0, 0, 0, 0, 0])
print(registers[0])


#%%
