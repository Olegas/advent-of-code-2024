from collections import defaultdict
from math import sqrt, log, ceil
from random import random, randint

import aocd
from aocd import submit
from tqdm import tqdm

data = aocd.data
data_ = """Register A: 30344604
Register B: 0
Register C: 0

Program: 2,4,1,1,7,5,1,5,4,5,0,3,5,5,3,0"""

registers_str, program_str = data.split('\n\n')
registers = dict()

for l in registers_str.splitlines():
    reg, val = l.split(': ')
    registers[reg[9:]] = int(val)
program = list([int(i) for i in program_str.replace('Program: ', '').split(',')])
print(registers)
print(program)


def computer(regs, code):
    ip = 0

    def as_combo(op):
        if 0 <= op <= 3:
            return op
        elif op == 4:
            return regs['A']
        elif op == 5:
            return regs['B']
        elif op == 6:
            return regs['C']
        raise ValueError(f'Incorrect combo op {op}')

    while True:
        if ip >= len(code):
            break
        opcode = code[ip]
        if opcode == 0:  # adv
            operand = code[ip + 1]
            op_value = as_combo(operand)
            n = regs['A']
            d = pow(2, op_value)
            regs['A'] = n // d
        elif opcode == 1:  # bxl
            op_value = code[ip + 1]
            regs['B'] = regs['B'] ^ op_value
        elif opcode == 2:  # bst
            operand = code[ip + 1]
            op_value = as_combo(operand)
            regs['B'] = op_value % 8
        elif opcode == 3:  # jnz
            if regs['A'] != 0:
                ip = code[ip + 1]
                continue
        elif opcode == 4:  # bxc
            regs['B'] = regs['B'] ^ regs['C']
        elif opcode == 5:  # out
            operand = code[ip + 1]
            op_value = as_combo(operand)
            yield op_value % 8
        elif opcode == 6:  # bdv
            operand = code[ip + 1]
            op_value = as_combo(operand)
            n = regs['A']
            d = pow(2, op_value)
            regs['B'] = n // d
        elif opcode == 7:  # cdv
            operand = code[ip + 1]
            op_value = as_combo(operand)
            n = regs['A']
            d = pow(2, op_value)
            regs['C'] = n // d
        ip += 2


def computer2(a):
    # number of iterations = ceil(log(a, 8))
    while a > 0:
        # this step number depends only on a % 8
        b2 = a % 8
        b2 = b2 ^ 1
        c = a // pow(2, b2)

        b = a % 8
        b = b ^ 1
        b = b ^ 5
        b = b ^ c

        a = a // 8
        yield b % 8


output = [str(i) for i in computer(registers.copy(), program)]
print(f'Part A: {",".join(output)}')

# Hint used: https://github.com/xhyrom/aoc/blob/main/2024/17/solution.py
# for given i, 8 * i + n, where n [0, 7]
# last numbers of generated sequence
# will be the same, as for sequence, generated from i
j = 124
print([d for d in computer2(j * 8 + 3)])
print([d for d in computer2(j)])

candidates = [0]
for l in range(1, len(program) + 1):
    next_c = []
    for c in candidates:
        for i in range(8):
            j = 2**3 * c + i
            res = [d for d in computer2(j)]
            if res == program[-l:]:
                next_c.append(j)
    candidates = next_c

print(f'Part B: {min(candidates)}')
print(program)
print([i for i in computer2(min(candidates))])