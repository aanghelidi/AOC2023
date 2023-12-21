import sys
import warnings
from typing import Generator

from scipy.optimize import curve_fit

warnings.filterwarnings("ignore")

with open(sys.argv[1]) as f:
    data = f.read().splitlines()


def adjacent4(pos: complex) -> Generator[complex, None, None]:
    yield pos + 1
    yield pos - 1
    yield pos + 1j
    yield pos - 1j


grid = {}
start = None
X = len(data[0])
Y = len(data)
for y, line in enumerate(data):
    for x, c in enumerate(line):
        if c == "S":
            start = complex(x, y)
            c = "."
        grid[complex(x, y)] = c

STEPS = 26501365
visited = {}
visited[0] = {start}
p_len = 0
cs = []
step = 0
while step < STEPS:
    for pos in visited[step]:
        for np in adjacent4(pos):
            cnp = complex(np.real % X, np.imag % Y)
            if grid.get(cnp, None) == ".":
                if step + 1 not in visited:
                    visited[step + 1] = set()
                visited[step + 1].add(np)
    if step % X == STEPS % X:
        cs.append(len(visited[step]))
    if len(cs) == 3:
        # we got enough data to fit the polynomial
        break
    step += 1


def poly(x, a, b, c):
    return a * x**2 + b * x + c


popt, _ = curve_fit(poly, [0, 1, 2], cs)
print(f"Part 2: {round(poly(STEPS // X, *popt))}")
