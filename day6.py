import aocd
from aocd import submit
from tqdm import tqdm

from util import field, inside, advance, apply, cw, north, vis

data = aocd.data
data_ = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

f, dim, idx = field(data, index=('^', '#'))
WALKED_AWAY = -1
LOOPED = -2


def simulate(fld, p, di, *, seen_states: set = None, seen_positions: set = None):
    if seen_states is None:
        seen_states = set()
    if seen_positions is None:
        seen_positions = set()
    while inside(p, dim):
        if (p, di) in seen_states:
            return LOOPED, None, None
        seen_positions.add(p)
        seen_states.add((p, di))
        fwd = advance(p, di)
        if fld[fwd] == '#':
            di = apply(di, cw)
        else:
            p = fwd

    return WALKED_AWAY, seen_positions


initial_pos = idx['^'].pop()
accu = 0
r, path = simulate(f, initial_pos, north)
print(f'Part A: {len(path)}')

for po in tqdm(path):
    if po == initial_pos:
        continue
    fld_with_obstacle = f.copy()
    fld_with_obstacle[po] = '#'
    r, *_ = simulate(fld_with_obstacle, initial_pos, north)
    if r == LOOPED:
        accu += 1

print(f'PartB: {accu}')
