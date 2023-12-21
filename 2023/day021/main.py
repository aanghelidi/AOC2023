import sys
from collections import deque
from typing import Generator

with open(sys.argv[1]) as f:
    data = f.read().splitlines()


def adjacent4(pos: complex) -> Generator[complex, None, None]:
    yield pos + 1
    yield pos - 1
    yield pos + 1j
    yield pos - 1j


grid = {}
start = None
for y, line in enumerate(data):
    for x, c in enumerate(line):
        if c == "S":
            start = complex(x, y)
            c = "."
        grid[complex(x, y)] = c

Q = deque([(0, start)])
visited = {(0, start)}
cs = {}
while Q:
    t, pos = Q.popleft()
    for np in adjacent4(pos):
        if np in grid and grid[np] == ".":
            if (t + 1, np) not in visited:
                if cs.get(t + 1) is None:
                    cs[t + 1] = 0
                cs[t + 1] += 1
                visited.add((t + 1, np))
                Q.append((t + 1, np))
    if 65 in cs:
        break

print(f"Part 1: {cs[64]}")
