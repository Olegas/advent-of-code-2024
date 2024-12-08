from itertools import permutations

import aocd
from aocd import submit
from tqdm import tqdm

from util import field, inside, advance, apply, cw, north

data = aocd.data
data_ = """T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
.........."""

freq_names = []
A = "A"
for i in range(0, 26):
    j = chr(ord(A) + i)
    freq_names.append(j)
    freq_names.append(j.lower())
for i in range(10):
    freq_names.append(str(i))

fld, dim, idx = field(data, index=freq_names)
antinodes = set()


def pt_mx_far(p1, p2, m):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1

    return x1 + m * dx, y1 + m * dy


def solve(part_b):
    for freq, positions in idx.items():
        assert len(positions) >= 2
        for pair in permutations(positions, 2):
            p1, p2 = pair
            m = 0 if part_b is True else 2
            while True if part_b else m == 2:
                anode = pt_mx_far(p1, p2, m)
                if inside(anode, dim):
                    antinodes.add(anode)
                    m += 1
                else:
                    break

    return len(antinodes)


print(f'Part A: {solve(False)}')
print(f'Part B: {solve(True)}')