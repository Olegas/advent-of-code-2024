from itertools import combinations

import aocd
import networkx as nx
from tqdm import tqdm

from util import lines

data = aocd.data
data_ = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

g = nx.Graph()

for l in lines(data):
    a, b = l.split('-')
    g.add_edge(a, b)


def solve_a():
    groups = set()
    candidates = [n for n in g.nodes if 't' == n[0]]
    for c in candidates:
        ns = list(g.neighbors(c))
        if len(ns) >= 2:
            for comb in combinations(ns, 2):
                if g.has_edge(*comb):
                    groups.add(tuple(sorted(tuple(comb) + (c,))))

    print(f'Part A: {len(groups)}')


def solve_b():
    for i in tqdm(range(100)):
        groups = set()
        for c in g.nodes:
            ns = list(g.neighbors(c))
            if len(ns) >= i:
                for comb in combinations(ns, i):
                    if all(g.has_edge(*c2) for c2 in combinations(comb, 2)):
                        groups.add(tuple(sorted(tuple(comb) + (c,))))
        if len(groups) == 1:
            print('Part B: ' + ','.join(sorted(groups.pop())))
            break


solve_a()
solve_b()
