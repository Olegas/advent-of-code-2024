from collections import defaultdict

import aocd
from aocd import submit
from tqdm import tqdm

from util import lines

data = aocd.data
data_ = """1
2
3
2024"""


def sequence(i, iters):
    yield i
    for _ in range(iters):
        r = i * 64
        i = i ^ r
        i = i % 16777216
        r = i // 32
        i = i ^ r
        i = i % 16777216
        r = i * 2048
        i = i ^ r
        i = i % 16777216
        yield i


def last_digit(n):
    for i in n:
        yield i % 10


def delta(n):
    prev = None
    for i in n:
        if prev is not None:
            yield i, i - prev
        prev = i


def pattern_and_price(n):
    pattern = tuple()
    for itm in n:
        price, delta = itm
        l = len(pattern)
        if l < 4:
            pattern = pattern + (delta,)
        if l == 3:
            yield pattern, price
            pattern = pattern[1:4]


def solve_a():
    accu = 0
    for number in lines(data):
        for last in sequence(int(number), 2000):
            pass
        accu += last
    return accu


def solve_b():
    prices_by_pattern = defaultdict(int)
    for number in tqdm(lines(data)):
        seen = set()
        for i in pattern_and_price(delta(last_digit(sequence(int(number), 2000)))):
            pattern, price = i
            if pattern not in seen:
                seen.add(pattern)
                prices_by_pattern[pattern] += price

    return max(prices_by_pattern.values())


print(f'Part A: {solve_a()}')
print(f'Part B: {solve_b()}')
