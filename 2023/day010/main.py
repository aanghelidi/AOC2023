import sys
from collections import Counter, defaultdict, deque
from typing import Generator

from rich import print

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

grid = {}
ans = 0
start = None
dist = defaultdict(lambda: sys.maxsize)
for y, line in enumerate(data):
    for x, pipe in enumerate(line):
        if pipe == "S":
            start = (x, y)
        grid[(x, y)] = pipe
        dist[(x, y)] = sys.maxsize


def adjacent_4_from_symbol(pos: tuple[int, int] | None, symbol: str) -> Generator[tuple, None, None]:
    x, y = pos
    if symbol == "S":
        symbol = "J"  # hardcoded from input
        # symbol = "7" # hardcoded from test input
    if symbol == "|":
        yield (x, y - 1)
        yield (x, y + 1)
    elif symbol == "-":
        yield (x - 1, y)
        yield (x + 1, y)
    elif symbol == "L":
        yield (x, y - 1)
        yield (x + 1, y)
    elif symbol == "J":
        yield (x, y - 1)
        yield (x - 1, y)
    elif symbol == "7":
        yield (x, y + 1)
        yield (x - 1, y)
    elif symbol == "F":
        yield (x, y + 1)
        yield (x + 1, y)
    else:
        raise ValueError(f"Unknown symbol: {symbol}")


queue = deque([(0, start)])
visited = set()
maxd = 0
while queue:
    steps, pos = queue.popleft()
    dist[pos] = steps
    maxd = max(maxd, steps)
    if pos in visited:
        continue
    visited.add(pos)
    for np in adjacent_4_from_symbol(pos, grid[pos]):
        pipe = grid.get(np)
        if pipe == "." or pipe is None:
            continue
        if np not in visited:
            queue.append((steps + 1, np))

print(f"Part 1: {maxd}")

bottom_right = max(grid.keys(), key=lambda x: x[0] + x[1])
visited_tiles = {k for k, v in dist.items() if v != sys.maxsize}
for y in range(bottom_right[1] + 1):
    n = 0
    for x in range(bottom_right[0] + 1):
        tile = grid.get((x, y))
        if (x, y) in visited_tiles:
            if tile in ("|", "L", "J", "S"):
                n += 1
            continue
        grid[(x, y)] = "O" if n % 2 == 0 else "I"

print(f"Part 2: {Counter(grid.values())['I']}")
