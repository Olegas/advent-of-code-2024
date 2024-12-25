from itertools import product, starmap

import aocd
from aocd import submit

from util import lines

data = aocd.data
data_ = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

KEY = 1
LOCK = 2

keys = []
locks = []
mode = None
item = [-1] * 5
for line in lines(data + '\n\n'):
    if mode is None:
        if line[0] == '.':
            mode = KEY
        elif line[1] == '#':
            mode = LOCK
        else:
            assert False
    if line == '':
        (keys if mode == KEY else locks).append(tuple(item))
        item = [-1] * 5
        mode = None
    else:
        for i, c in enumerate(line):
            if c == '#':
                item[i] += 1


def is_fit(a, b):
    return all(map(lambda i: i <= 5, [i + j for i, j in zip(a, b)]))


print(sum(is_fit(*i) for i in product(keys, locks)))
