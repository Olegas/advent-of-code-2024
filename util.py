from collections import defaultdict


def lines(d):
    return d.splitlines()


def field(d):
    r = defaultdict(lambda: '.')
    lns = lines(d)
    for y, l in enumerate(lns):
        for x, c in enumerate(list(l)):
            r[x, y] = c
    d = (len(lns[0]), len(lns))
    return r, d


def arrays_of_numbers(d):
    return [[int(i) for i in l.split(' ')] for l in lines(d)]
