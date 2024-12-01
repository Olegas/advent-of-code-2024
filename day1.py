import aocd
from aocd import submit
from collections import Counter

data = aocd.data
data_ = """3   4
4   3
2   5
1   3
3   9
3   3"""

lines = map(lambda i: i.split(' '), data.splitlines())
list1 = []
list2 = []
for i in lines:
    list1.append(int(i[0]))
    list2.append(int(i[-1]))

list1 = sorted(list1)
list2 = sorted(list2)

assert len(list1) == len(list2)

s = 0
for k in range(0, len(list1)):
    s += abs(list1[k] - list2[k])
submit(s, part='a')

c = Counter(list2)
s = 0
for i in list1:
    s += i * c[i]

submit(s, part='b')
