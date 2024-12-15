import time
from collections import Counter
import aocd

from util import field, vis, move_to_dp, advance, east, west

data = aocd.data
data_ = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

data_ = """#######
#.....#
#.....#
#.@O..#
#..#O.#
#...O.#
#..O..#
#.....#
#######

>><vvv>v>^^^"""


def expand_field(s):
    s = s.replace('#', '##')
    s = s.replace('.', '..')
    s = s.replace('@', '@.')
    return s.replace('O', '[]')


def solve_a(data):
    p = data.index('\n\n')
    fld, dim, idx = field(data[:p + 1], index=('#', 'O', '@'))
    moves = data[p + 2:]

    p = idx['@'].pop()
    fld[p] = '.'
    for idx, m in enumerate(moves):
        if m == '\n':
            continue
        dp = move_to_dp[m]
        np = advance(p, dp)
        if fld[np] == '.':
            p = np
        elif fld[np] == '#':
            continue
        elif fld[np] == 'O':
            lp = np
            first_box = np
            last_box = np
            commit_move = True
            while True:
                lp = advance(lp, dp)
                if fld[lp] == '.':
                    break
                elif fld[lp] == 'O':
                    last_box = lp
                elif fld[lp] == '#':
                    commit_move = False
                    break
            if commit_move:
                fld.pop(first_box)
                next_last_pos = advance(last_box, dp)
                if fld[next_last_pos] != '.':
                    print(idx)
                    vis(fld, dim, {})
                    exit(-1)
                fld[next_last_pos] = 'O'
                p = np

    return sum([100 * p[1] + p[0] for p, v in fld.items() if v == 'O'])


def solve_b(data):
    data = expand_field(data)
    p = data.index('\n\n')
    fld, dim, idx = field(data[:p + 1], index=('@',))
    moves = data[p + 2:]

    p = idx['@'].pop()
    np = None
    c = 0
    fld[p] = '.'
    cc = Counter()
    for v in fld.values():
        cc[v] += 1
    print(cc)
    for idx, m in enumerate(moves):
        if m == '\n':
            continue
        c += 1
        dp = move_to_dp[m]
        # clear_screen()
        # vis(fld, dim, {p: '@'})
        # time.sleep(0.5)
        np = advance(p, dp)
        if fld[np] == '.':
            p = np
        elif fld[np] == '#':
            continue
        elif fld[np] in ('[', ']'):
            box_coord_set = collect_boxes(fld, np, dp)
            if can_move(fld, box_coord_set, dp):
                move_boxes(fld, box_coord_set, dp)
                p = np
            else:
                pass

    print(f'Moves: {c}')
    cc = Counter()
    for v in fld.values():
        cc[v] += 1
    print(cc)
    # vis(fld, dim, {p: '@'})
    return sum([100 * p[1] + p[0] for p, v in fld.items() if v == '['])


def move_boxes(fld, coord_set, dp):
    which = dict()
    for c in coord_set:
        assert fld[c] in ('[', ']')
        nc = advance(c, dp)
        which[nc] = fld[c]
        fld.pop(c)
    assert len(coord_set) == len(which)
    for c, b in which.items():
        fld[c] = b


def is_free(fld, pos, dp) -> bool:
    next_pt = advance(pos, dp)
    if fld[next_pt] != '.':
        return False
    return True


def can_move(fld, coord_set, dp) -> bool:
    for p in coord_set:
        # Used edge-case from here:
        # https://www.reddit.com/r/adventofcode/comments/1hetkud/year_2024day_15_extra_test_case_to_help_with_part/
        np = advance(p, dp)
        if fld[np] == '#':
            return False

    return True


def collect_boxes(fld, start, dp) -> set:
    d = set()

    def explore(p):
        pt = fld[p]
        if pt == '[':
            d.add(p)
            explore(advance(p, dp))
            np = advance(p, east)
            assert fld[np] == ']'
            if np not in d:
                explore(np)
        elif pt == ']':
            d.add(p)
            explore(advance(p, dp))
            np = advance(p, west)
            assert fld[np] == '['
            if np not in d:
                explore(np)
        else:
            pass

    explore(start)
    return d


print(f'Part A: {solve_a(data)}')
print(f'Part B: {solve_b(data)}')
