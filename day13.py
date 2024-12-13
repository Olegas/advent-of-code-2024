import numpy as np

import aocd
from aocd import submit

from util import lines

data = aocd.data
data_ = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

machines = []
m = [None] * 3
for idx, line in enumerate(lines(data)):
    p = idx % 4
    if p in (0, 1, 2):
        _, c = line.split(': ')
        xs, ys = c.split(', ')
        x = int(xs[2:])
        y = int(ys[2:])
        m[p] = (x, y)
        if p == 2:
            machines.append(m)
            m = [None] * 3


def solve(part_b=False):
    accu = 0
    count = 0
    inc = 10000000000000 if part_b else 0
    for idx, m in enumerate(machines):
        ax, ay = m[0]
        bx, by = m[1]
        tx, ty = m[2]
        a = np.array([[ax, bx], [ay, by]])
        b = np.array([tx + inc, ty + inc])
        x = np.linalg.solve(a, b)
        if abs(x[0] - round(x[0])) < 1e-2 and abs(x[1] - round(x[1])) < 1e-2:
            count += 1
            accu += 3 * round(x[0]) + round(x[1])

    print(count, int(accu))


solve()
solve(True)
