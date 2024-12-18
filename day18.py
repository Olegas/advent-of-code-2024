from math import inf
from collections import defaultdict

import aocd
from aocd import submit
from tqdm import tqdm

from util import around, advance, inside, vis

data = aocd.data
data_ = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
dim = (71, 71)
max_b = 1024

fld = defaultdict(lambda: '.')
lines = data.splitlines()
initial_bytes = lines[:max_b]
next_bytes = lines[max_b:]
for idx, line in enumerate(initial_bytes):
    xs, ys = line.split(',')
    p = (int(xs), int(ys))
    fld[p] = '#'

start = (0, 0)
end_pos = (dim[0] - 1, dim[1] - 1)


def walk_to_exit():
    cost = defaultdict(lambda: +inf)

    def step():
        heads = [(start, 0)]
        while heads:
            head = heads.pop()
            p, c = head
            for dp in around:
                np = advance(p, dp)
                nc = c + 1
                if inside(np, dim) and nc < cost[np] and fld[np] != '#':
                    cost[np] = nc
                    heads.append((np, nc))

    step()

    cost[start] = 0
    if cost[end_pos] != +inf:
        p = end_pos
        path = {end_pos}
        c = cost[end_pos]
        while p != start:
            for dp in around:
                np = advance(p, dp)
                if inside(np, dim) and cost[np] == c - 1 and fld[np] != '#':
                    path.add(np)
                    p = np
                    c -= 1
                    break
        return path
    return None


initial_short_path = walk_to_exit()
print(f'Part A: {len(initial_short_path) - 1}')

for line in tqdm(next_bytes):
    xs, ys = line.split(',')
    b = (int(xs), int(ys))
    fld[b] = '#'
    if b in initial_short_path:
        next_short_path = walk_to_exit()
        if next_short_path is None:
            print(f'Part B: {b}')
            break
        else:
            initial_short_path = next_short_path
