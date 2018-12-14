#%%
from typing import NamedTuple, List, Dict, Set, Tuple
from collections import defaultdict, Counter

test_line = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


class Node(NamedTuple):
    n_childs: int
    n_metadata: int
    childs: List[Node]
    metadata: List[int]
    value: int


def find_next_leaf(data: List[int]) -> int:
    return min([i for i, d in enumerate(data) if d == 0 and i % 2 == 0])


def get_node(data: List[int], is_root=True) -> Tuple[Node, List[int]]:
    stack: List[Node]

    n_childs = data[0]
    n_metadata = data[1]
    data = data[2:]

    childs: List[Node] = []

    while len(childs) < n_childs:
        child, data = get_node(data, is_root=False)
        childs.append(child)

    metadata = data[:n_metadata]

    if n_childs == 0:
        value = sum(metadata)
    else:
        value = sum(
            [childs[i - 1].value for i in metadata if i - 1 in range(len(childs))]
        )

    node = Node(n_childs, n_metadata, childs, metadata, value)

    data = data[n_metadata:]

    if is_root:
        assert len(data) == 0

    return node, data


data = [int(n) for n in test_line.split()]
node, _ = get_node(data)

#%%
def sum_metadata(node: Node) -> int:
    return sum(node.metadata) + sum([sum_metadata(n) for n in node.childs])


assert sum_metadata(node) == 138

#%%
with open("input.txt", "r") as f:
    line = f.read()

data = [int(n) for n in line.split()]
node, _ = get_node(data)
print(f"Metadata sum is {sum_metadata(node)}")

#%%
data = [int(n) for n in test_line.split()]
node, _ = get_node(data)

assert node.value == 66
#%%
data = [int(n) for n in line.split()]
node, _ = get_node(data)

print(f"Root node value is {node.value}")

#%%
