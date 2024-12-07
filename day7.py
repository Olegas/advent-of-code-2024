import itertools
import operator as op
from functools import reduce

import aocd
from aocd import submit
from tqdm import tqdm

from util import lines

data = aocd.data
data_ = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def solve(ops):
    accu = 0
    for l in tqdm(lines(data)):
        t, rest = l.split(': ')
        t = int(t)
        values = [int(i) for i in rest.split(' ')]
        variants = itertools.product(ops, repeat=len(values) - 1)
        for v in variants:
            r = reduce(lambda m, i: i[0](m, i[1]), zip(v, values[1:]), values[0])
            if t == r:
                accu += t
                break

    return accu


def concat(a, b):
    return int(f'{a}{b}')


a = solve([op.add, op.mul])
b = solve([op.add, op.mul, concat])

print(f'Part A: {a}')
print(f'Part B: {b}')
