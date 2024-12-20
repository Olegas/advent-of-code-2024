from math import inf
from collections import defaultdict, Counter

import aocd
from aocd import submit
from tqdm import tqdm

from util import around, advance, inside, vis, field

data = aocd.data
data_ = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

fld, dim, idx = field(data, index=('S', 'E'))
start = idx['S'].pop()
end_pos = idx['E'].pop()


def walk_to_exit(fr, to):
    cost = defaultdict(lambda: +inf)

    def step():
        heads = [(fr, 0)]
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

    cost[fr] = 0
    if cost[to] != +inf:
        p = to
        path = {to}
        c = cost[to]
        while p != fr:
            for dp in around:
                np = advance(p, dp)
                if inside(np, dim) and cost[np] == c - 1 and fld[np] != '#':
                    path.add(np)
                    p = np
                    c -= 1
                    break
        return path, cost
    return None, None


def find_cheats(from_pos, path, cost_dict, max_len):
    count_by_saved_dist = Counter()
    x, y = from_pos
    candidates = set()
    for dx in range(-max_len - 1, max_len + 1):
        for dy in range(-max_len - 1, max_len + 1):
            if dx == 0 and dy == 0:
                continue
            if abs(dx) + abs(dy) <= max_len and inside((x + dx, y + dy), dim):
                candidates.add((x + dx, y + dy))
    intersections = candidates.intersection(path)
    for p in intersections:
        original_distance = cost_dict[p] - cost_dict[from_pos]
        if original_distance < 0:
            continue
        px, py = p
        current_distance = abs(px - x) + abs(py - y)
        assert current_distance <= max_len
        if current_distance < original_distance:
            saved = original_distance - current_distance
            count_by_saved_dist[saved] += 1

    return count_by_saved_dist


def solve(min_save, max_dist):
    path, cost_dict = walk_to_exit(start, end_pos)
    counter = Counter()
    for p in tqdm(path):
        count_by_saved_dist = find_cheats(p, path, cost_dict, max_dist)
        counter.update(count_by_saved_dist)

    accu = sum(n for k, n in counter.items() if k >= min_save)
    print(accu)


solve(100, 2)
solve(100, 20)
