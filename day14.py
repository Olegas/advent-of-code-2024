import os
from collections import Counter
import time
from functools import reduce

import aocd
from aocd import submit
from tqdm import tqdm

from util import lines, advance

data = aocd.data
data_ = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

dim = (101, 103)

robots = []
for line in lines(data):
    ps, vs = line.strip().split(' ')
    p = tuple(map(int, ps[2:].split(',')))
    v = tuple(map(int, vs[2:].split(',')))
    robots.append((p, v))


def move(r, d):
    p, v = r
    dix, diy = d
    nx, ny = advance(p, v)
    return (nx % dix, ny % diy), v


def simulate(s, r):
    for i in range(s):
        r = [move(r, dim) for r in r]

    return r


def split(rs):
    c = Counter()
    for r in rs:
        c[r[0]] += 1
    dix, diy = dim
    quadrants = [0] * 4
    for p, cnt in c.items():
        x, y = p
        if x == dix // 2 or y == diy // 2:
            continue
        qx = 0 if x < dix // 2 else 1
        qy = 0 if y < diy // 2 else 1
        quadrants[qx + 2 * qy] += cnt
    return reduce(lambda m, i: m * i, quadrants, 1)


print(f'Part A: {split(simulate(100, robots))}')


def tree_founder(r):
    dix, diy = dim
    for iter in tqdm(range(10000000000)):
        r = [move(r, dim) for r in r]
        ps = {ri[0] for ri in r}

        for y in range(diy):
            ps_here = sorted(list(p[0] for p in ps if p[1] == y))
            for ca in ps_here:
                for i in range(dix):
                    if ca + i not in ps_here:
                        break
                if i > 8:
                    for y in range(diy):
                        print('')
                        for x in range(dix):
                            print('#' if (x, y) in ps else '.', end='')
                    print(iter + 1)
                    input("Press Enter to continue...")
                    print(chr(27) + "[2J")


tree_founder(robots)
