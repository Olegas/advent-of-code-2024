from collections import defaultdict

import aocd
from itertools import product
from util import field as get_field

data = aocd.data
data_ = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
.........."""

field, dimension = get_field(aocd.data)
around = set(product([-1, 0, 1], repeat=2)) - {(0, 0)}
around_x = (
    (
        ((-1, -1), (0, 0), (1, 1)),
        ((-1, 1), (0, 0), (1, -1))
    ),  # x
)
next_c = {
    'X': 'M',
    'M': 'A',
    'A': 'S'
}


def solve_a(f, dim):
    accu = 0
    mx, my = dim
    for y in range(0, my):
        for x in range(0, mx):
            c = f[x, y]
            if c == 'X':
                for dp in around:
                    dx, dy = dp
                    w = ''
                    for i in range(4):
                        w += f[x + dx * i, y + dy * i]
                    if w == 'XMAS':
                        accu += 1
    return accu


def solve_b(f, dim):
    accu = 0
    mx, my = dim
    for y in range(0, my):
        for x in range(0, mx):
            c = f[x, y]
            if c == 'A':
                for variant in around_x:
                    c_lines = 0
                    for line in variant:
                        w = ''
                        for dp in line:
                            dx, dy = dp
                            w += f[x + dx, y + dy]
                        if w in ('MAS', 'SAM'):
                            c_lines += 1
                    if c_lines == 2:
                        accu += 1

    return accu


print(solve_a(field, dimension))
print(solve_b(field, dimension))
