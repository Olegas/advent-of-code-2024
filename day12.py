import json
from collections import Counter
from itertools import combinations
import aocd
from util import field, all_capital_letters, advance, around, hor, ver, full_round

# Hint used: https://www.reddit.com/r/adventofcode/comments/1hcf16m/2024_day_12_everyone_must_be_hating_today_so_here/

data = aocd.data
data_ = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

fld, dim, idx = field(data, index=all_capital_letters())


def calc_perimeter(reg: set):
    xs = [p[0] for p in reg]
    min_x = min(xs)
    max_x = max(xs)

    ys = [p[1] for p in reg]
    min_y = min(ys)
    max_y = max(ys)

    accu = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            p = (x, y)
            if p not in reg:
                continue
            shell_pts = {advance(p, dp) for dp in full_round if advance(p, dp) not in reg}
            accu += sum(s not in reg for s in shell_pts)

    count_lines = detect_lines(reg)

    return accu, count_lines


def detect_lines(region: set) -> int:
    cnt = 0
    for p in region:
        candidates = set()
        for d in around:
            np = advance(p, d)
            if np in region:
                candidates.add(d)
        if len(candidates) == 0:
            cnt += 4
        elif len(candidates) == 1:
            # point starts a single line
            cnt += 2
        elif len(candidates) == 2:
            if candidates == hor or candidates == ver:
                continue
            cnt += 1
            a, b = candidates
            ins = advance(advance(p, a), b)
            if ins not in region:
                # inner corner
                cnt += 1
        elif len(candidates) == 3 or len(candidates) == 4:
            for c in combinations(candidates, 2):
                a, b = c
                ins = advance(advance(p, a), b)
                if ins not in region:
                    # inner corner
                    cnt += 1
        else:
            assert False

    return cnt


def detect_subregions(reg: set) -> list[set]:
    regs = []
    while len(reg):
        any_coord = reg.pop()
        subreg = {any_coord}
        heads = {any_coord}
        while heads:
            next_heads = set()
            for head in heads:
                for dp in around:
                    np = advance(head, dp)
                    if np in reg:
                        subreg.add(np)
                        reg.remove(np)
                        next_heads.add(np)
            heads = next_heads
        regs.append(subreg)
    return regs


accu_a = 0
accu_b = 0
regions = []
c = Counter()
for id, reg in idx.items():
    c[id] += 1
    regions.extend([(id, r) for r in detect_subregions(reg)])

for r in regions:
    id, reg = r
    area = len(reg)
    perimeter, sides = calc_perimeter(reg)
    print(f'{id}: A: {area} * {perimeter} = {area * perimeter}')
    print(f'   B: {area} * {sides} = {area * sides}')
    accu_a += area * perimeter
    accu_b += area * sides

print(accu_a, accu_b)

state = {
    "regs": c,
    "dim": dim,
    "data": list(map(lambda i: [i[0], list(i[1])], regions))
}

with open('state.json', 'wt') as f:
    f.write(json.dumps(state))
