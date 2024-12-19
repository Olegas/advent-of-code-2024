import functools

import aocd
from aocd import submit

data = aocd.data
data_ = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

lines = data.split('\n')
towels = tuple(lines[0].split(', '))
designs = lines[2:]


@functools.cache
def solve(dis):
    n_ways = 0
    if dis == '':
        return 1
    for a in towels:
        if dis[:len(a)] == a:
            n = dis[len(a):]
            n_ways += solve(n)
    return n_ways


accu_a = 0
accu_b = 0
for d in designs:
    res = solve(d)
    accu_b += res
    if res > 0:
        accu_a += 1
print(f'Part A: {accu_a}\nPart B: {accu_b}')
