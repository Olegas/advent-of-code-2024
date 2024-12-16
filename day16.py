from collections import defaultdict
from math import inf

import aocd
from heapq import heapify, heappop, heappush
from aocd import submit
from tqdm import tqdm

from util import field, east, advance, apply, cw, ccw, vis, clear_screen, none

data = aocd.data
data1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

data2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

fld, dim, idx = field(data, index=('S', 'E'))

paths = []
heapify(paths)
start_pos = idx['S'].pop()
end_pos = idx['E'].pop()
heappush(paths, (0, {start_pos}, east, start_pos))

score_at_pos = defaultdict(lambda: +inf)
total_len = defaultdict(lambda: set())
while paths:
    head = heappop(paths)
    score, seen, dp, p = head
    if p == end_pos:
        total_len[score] |= seen
    variances = ((none, 1), (cw, 1001), (ccw, 1001))
    for v in variances:
        rotation, penalty = v
        ndp = apply(dp, rotation)
        np = advance(p, ndp)
        ns = score + penalty
        if np not in seen and fld[np] != '#':
            flt_key = (np, ndp)
            if score_at_pos[flt_key] >= ns:
                heappush(paths, (ns, seen | {np}, ndp, np))
            score_at_pos[flt_key] = min(score_at_pos[flt_key], ns)


min_p = min(total_len.keys())
print(f'Part A: {min_p}')
print(f'Part B: {len(total_len[min_p])}')


