from collections import defaultdict
import aocd
from util import field, around, advance

data = aocd.data
data_ = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

fld, dim, idx = field(data, index=(0,), transform=int)


def walk(f, p):
    assert f[p] == 0
    ratings = defaultdict(lambda: 0)
    paths = [({p}, p, 0)]
    while len(paths) > 0:
        path = paths.pop()
        seen, head, level = path
        if level == 9:
            ratings[head] += 1
            continue
        for dd in around:
            np = advance(head, dd)
            if f[np] == level + 1 and np not in seen:
                paths.append((seen | {np}, np, level + 1))
    return ratings


def solve():
    scores = 0
    ratings = defaultdict(lambda: 0)
    for pos in idx[0]:
        r = walk(fld, pos)
        scores += len(r.keys())
        for k, v in r.items():
            ratings[k] += v
    return scores, sum(ratings.values())


part_a, part_b = solve()
print(f'Part A: {part_a}\nPart B: {part_b}')
