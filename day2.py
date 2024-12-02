from functools import reduce

import aocd

data = aocd.data
data_ = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

lines = list(
    map(lambda i: list(map(int, i)),
        map(lambda i: i.split(' '), data.splitlines())))


def is_safe(l, can_retry):
    directions = [True] * len(l)
    diffs = []
    for i in range(0, len(l)):
        a = l[i]
        diffs.append(1 <= abs(a - l[i + 1]) <= 3 if i == 0 else 1 <= abs(a - l[i - 1]) <= 3)
    if len(l) > 2:  # Таких данных нет (кол-во элементов <= 2). Оставил для локальных тестов
        for i in range(0, len(l)):
            if i == 0:
                directions[i] = (l[i] < l[i + 1]) == (l[i + 1] < l[i + 2])
            elif i == len(l) - 1:
                directions[i] = (l[i - 2] < l[i - 1]) == (l[i - 1] < l[i])
            else:
                directions[i] = (l[i - 1] < l[i]) == (l[i] < l[i + 1])
    have_errors = False
    for i in range(0, len(l)):
        if directions[i] is False or diffs[i] is False:
            if can_retry:
                try_remove = is_safe(l[0:i] + l[i + 1:], False)
                if try_remove:
                    return True
                have_errors = True
            else:
                return False

    return not have_errors


def solve(tolerate_errors):
    safe = reduce(lambda m, l: m + is_safe(l, tolerate_errors), lines, 0)
    print(safe)


def part_a():
    solve(False)


def part_b():
    solve(True)


part_a()
part_b()
