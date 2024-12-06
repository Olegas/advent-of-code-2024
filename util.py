from collections import defaultdict


def lines(d):
    return d.splitlines()


def field(d, *, index=None):
    r = defaultdict(lambda: '.')
    lns = lines(d)
    i = defaultdict(lambda: set())
    for y, l in enumerate(lns):
        for x, c in enumerate(list(l)):
            if index is not None and c in index:
                i[c].add((x, y))
            r[x, y] = c
    d = (len(lns[0]), len(lns))
    return r, d, i


def arrays_of_numbers(d):
    return [[int(i) for i in l.split(' ')] for l in lines(d)]


north = (0, -1)

cw = {
    (0, -1): (1, 0),
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1)
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
