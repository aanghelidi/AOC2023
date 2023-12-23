import sys
from typing import Generator

import networkx as nx

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

grid = {}
start = None
end = None
n = len(data)
for y, line in enumerate(data):
    for x, c in enumerate(line):
        if y == 0 and c == ".":
            start = complex(x, y)
        if y == n - 1 and c == ".":
            end = complex(x, y)
        grid[complex(x, y)] = c

east = lambda pos: pos + 1
west = lambda pos: pos - 1
south = lambda pos: pos + 1j
north = lambda pos: pos - 1j
slopesmap = dict(zip("^>v<", [north, east, south, west]))


def adjacent4(pos: complex) -> Generator[complex, None, None]:
    yield north(pos)
    yield east(pos)
    yield south(pos)
    yield west(pos)


G = nx.DiGraph()
for pos, c in grid.items():
    if c == ".":
        nps = list(adjacent4(pos))
        if len(nps) == 1 and pos != start and pos != end:
            G.remove_node(pos)
            continue
        if len(nps) == 0:
            G.remove_node(pos)
            continue
        G.add_node(pos)
        for adj in adjacent4(pos):
            if adj in grid and (grid[adj] == "." or grid[adj] in "^>v<"):
                G.add_edge(pos, adj)
    elif c in "^>v<":
        G.add_node(pos)
        # Part 2: treat slopes as regular nodes
        nps = list(adjacent4(pos))
        if len(nps) == 1 and pos != start and pos != end:
            G.remove_node(pos)
            continue
        if len(nps) == 0:
            G.remove_node(pos)
            continue
        for adj in adjacent4(pos):
            if adj in grid and (grid[adj] == "." or grid[adj] in "^>v<"):
                G.add_edge(pos, adj)
        # Part 1
        # G.add_edge(pos, slopesmap[c](pos))

# nx.nx_pydot.write_dot(G, "graph.dot")

# all_paths = nx.all_simple_paths(G, end, start)
# print(max(len(p) - 1 for p in all_paths))
for p in nx.all_simple_paths(G, end, start):
    # Reverse brute force : 6394
    print(len(p) - 1)
