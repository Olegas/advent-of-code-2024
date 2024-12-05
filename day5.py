import traceback
from math import ceil, floor

import aocd
from aocd import submit
from util import lines
import networkx as nx

data = aocd.data
data_ = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

g = nx.DiGraph()
phase = 0
mid = 0
mid2 = 0
incorrect = []
for l in lines(data):
    if phase == 0:
        if l.strip() == '':
            phase = 1
            continue
        a, b = l.split('|')
        g.add_edge(a, b)
    else:
        nodes = l.split(',')
        ok = True
        for pair in zip(nodes, nodes[1:]):
            a, b = pair
            try:
                p = nx.shortest_path(g, a, b)
                if len(p) != 2:
                    # BUT WHAAAAAAAAY???????
                    ok = False
                    break
                # print(f'p bw {a} & {b} -> {p}')
            except nx.NetworkXNoPath as e:
                print(f'{l} incorrect bc {a}->{b}: {e}')
                ok = False
                break
        if ok:
            assert len(nodes) % 2 == 1
            mid += int(nodes[floor(len(nodes) / 2)])
        else:
            sub = nx.subgraph(g, nodes)
            topo = list(nx.topological_sort(sub))
            mid2 += int(topo[floor(len(topo) / 2)])

print(f'Part A {mid}')
print(f'Part B {mid2}')


