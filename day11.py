from collections import Counter
from math import floor, log10

import aocd
from aocd import submit

from util import array_of_numbers

data = aocd.data
data_ = """125 17"""


def mutate(n):
    if n == 0:
        return 1,
    elif (digits := floor(log10(n) + 1)) % 2 == 0:
        d = pow(10, (int(digits / 2)))
        return divmod(n, d)
    else:
        return n * 2024,


def solve(blinks):
    c = Counter(array_of_numbers(data))
    for i in range(blinks):
        c2 = Counter()
        for v, cnt in c.items():
            r = mutate(v)
            for nn in r:
                c2[nn] += cnt
        c = c2
    return sum(c.values())


print(f'Part A: {solve(25)}\nPart B: {solve(75)}')
