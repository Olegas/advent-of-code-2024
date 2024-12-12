from collections import defaultdict


def lines(d):
    return d.splitlines()


def field(d, *, index=None, transform=None):
    r = defaultdict(lambda: '.')
    lns = lines(d)
    i = defaultdict(lambda: set())
    for y, l in enumerate(lns):
        for x, c in enumerate(list(l)):
            c = transform(c) if transform is not None and c != '.' else c
            if index is not None and c in index:
                i[c].add((x, y))
            r[x, y] = c
    d = (len(lns[0]), len(lns))
    return r, d, i


def array_of_numbers(d):
    return [int(i) for i in d.split(' ')]


def arrays_of_numbers(d):
    return [[int(i) for i in l.split(' ')] for l in lines(d)]


north = (0, -1)
nw = (-1, -1)
ne = (1, -1)
south = (0, 1)
sw = (-1, 1)
se = (1, 1)
west = (-1, 0)
east = (1, 0)
full_round = (north, south, west, east, nw, ne, sw, se)
around = (north, south, west, east)
hor = {west, east}
ver = {north, south}

cw = {
    north: east,
    east: south,
    south: west,
    west: north
}

ccw = {
    north: west,
    west: south,
    south: east,
    east: north
}


def inside(p, dim):
    mx, my = dim
    x, y = p
    return 0 <= x < mx and 0 <= y < my


def apply(p, r):
    return r[p]


def advance(p, d):
    x, y = p
    dx, dy = d
    return x + dx, y + dy


def vis(f, dim, draw_map):
    mx, my = dim
    for y in range(my):
        print('')
        for x in range(mx):
            cc = draw_map.get((x, y)) or f[x, y]
            print(cc, end='')
    print('')


def all_capital_letters():
    return [chr(ord('A') + i) for i in range(0, 26)]


def all_small_letters():
    return [chr(ord('a') + i) for i in range(0, 26)]


def all_digits():
    return [str(i) for i in range(10)]
