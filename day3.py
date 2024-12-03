import aocd
from aocd import submit

data = aocd.data
data_ = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
data_ = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""


def read_num(i, data):
    op = ''
    while data[i].isdigit():
        op += data[i]
        i += 1
    if 1 <= len(op) <= 3:
        return i, int(op)
    return i, None


def solve(part_b):
    accu = 0
    allow = True
    for i, c in enumerate(data):
        if data[i:i + 2] == 'do':
            if data[i:i + 4] == 'do()':
                allow = True
            elif data[i:i + 7] == "don't()":
                allow = False
        if data[i:i + 3] == 'mul':
            if data[i + 3] != '(':
                continue
            ni, op1 = read_num(i + 4, data)
            if op1 is None:
                continue
            if data[ni] != ',':
                continue
            ni, op2 = read_num(ni + 1, data)
            if op2 is None:
                continue
            if data[ni] != ')':
                continue
            if part_b and not allow:
                continue
            accu += op1 * op2
    return accu


print(solve(False))
print(solve(True))
