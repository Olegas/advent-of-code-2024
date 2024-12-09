from dataclasses import dataclass
from typing import Optional, Tuple

import aocd
from tqdm import tqdm

data = aocd.data
data_ = """2333133121414131402"""


@dataclass
class Value:
    id: int
    type: str
    size: int


@dataclass(kw_only=True)
class Node:
    prev: Optional['Node']
    next: Optional['Node']
    value: Value


def load() -> Tuple[Node, Node]:
    prev: Node | None = None
    first: Node | None = None
    last: Node | None = None
    file_id = -1
    for idx, blk in enumerate(data):
        is_file = idx % 2 == 0
        if is_file:
            file_id += 1
        value = Value(
            id=file_id if is_file else None,
            type='f' if is_file else '.',
            size=int(blk)
        )
        new = Node(prev=prev, next=None, value=value)
        if idx == 0:
            first = new
        if prev is not None:
            prev.next = new
        prev = new
        last = new
    return first, last


def print_list(head: Node):
    ptr = head
    while ptr is not None:
        print(str(ptr.value.id if ptr.value.type == 'f' else '.') * ptr.value.size, end='')
        ptr = ptr.next
    print('')


def next_free_block(head: Node) -> Optional[Node]:
    ptr = head
    while ptr:
        if ptr.value.type == '.':
            return ptr
        ptr = ptr.next
    return None


def prev_file_block(head: Node) -> Optional[Node]:
    ptr = head
    while ptr:
        if ptr.value.type == 'f':
            return ptr
        ptr = ptr.prev
    return None


def remove(head):
    p = head.prev
    n = head.next
    p.next = n
    n.prev = p


def split_block(head, right_size) -> Tuple[Node, Node]:
    assert head.value.size > right_size
    new_node = Node(prev=None, next=None,
                    value=Value(id=head.value.id, type=head.value.type, size=head.value.size - right_size))
    insert_before(head, new_node)
    head.value.size = right_size
    return new_node, head


def insert_before(head: Node, node: Node):
    node_prev = node.prev
    node_next = node.next

    if node_next is not None:
        node_next.prev = node_prev
    if node_prev is not None:
        node_prev.next = node_next

    head_prev = head.prev

    head_prev.next = node
    node.prev = head_prev

    node.next = head
    head.prev = node


def exchange(b1: Node, b2: Node):
    assert b1.value.type != b2.value.type
    _v = b1.value
    b1.value = b2.value
    b2.value = _v


def join(b1: Node, b2: Node):
    assert b1.value.type == '.'
    assert b1.value.type == b2.value.type
    assert b1.next == b2
    b1.value.size += b2.value.size
    remove(b2)


def crc(head: Node) -> int:
    ptr = head
    idx = 0
    accu = 0
    while ptr:
        if ptr.value.type == 'f':
            block_s = (2 * idx + (ptr.value.size - 1)) / 2 * ptr.value.size
            accu += block_s * ptr.value.id
        idx += ptr.value.size
        ptr = ptr.next
    return int(accu)


def solve_a():
    head, tail = load()
    free_block = next_free_block(head)
    assert free_block.value.type == '.'
    file_block = prev_file_block(tail)
    assert file_block.value.type == 'f'

    while True:
        # print_list(head)
        if free_block.value.size == file_block.value.size:
            exchange(file_block, free_block)
            free_block = next_free_block(free_block.next)
            file_block = prev_file_block(file_block)
            if id(free_block.prev) == id(file_block):
                break
        elif free_block.value.size > file_block.value.size:
            free_block, free_block_remain = split_block(free_block, free_block.value.size - file_block.value.size)
        else:  # free_block.value.size < file_block.value.size
            block_to_remain, file_block = split_block(file_block, free_block.value.size)

    return crc(head)


def solve_b():
    head, tail = load()
    ptr = head
    index = []
    while ptr is not None:
        if ptr.value.type == 'f':
            index.append((ptr.value.id, ptr))
            pass
        ptr = ptr.next

    index.sort(key=lambda i: i[0], reverse=True)
    for item in tqdm(index):
        _, file = item
        ptr = head
        req_size = file.value.size
        while ptr is not None and id(ptr) != id(file):
            if ptr.value.type == '.' and ptr.value.size >= req_size:
                if ptr.value.size == req_size:
                    exchange(ptr, file)
                else:  # ptr.value.size > req_size
                    fit, excess = split_block(ptr, ptr.value.size - req_size)
                    exchange(fit, file)
                    if excess.next.value.type == '.':
                        join(excess, excess.next)
                break
            else:
                ptr = ptr.next
    return crc(head)


print(solve_a())
print(solve_b())
