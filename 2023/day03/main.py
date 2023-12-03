import itertools
import math
import sys
from dataclasses import dataclass
from typing import Generator

with open(sys.argv[1]) as f:
    data = f.read().splitlines()


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class PartNumber:
    value: int
    start: Point
    stop: Point


def adjacent8(p: Point) -> Generator[Point, None, None]:
    for x_offset, y_offset in itertools.product([-1, 0, 1], repeat=2):
        if x_offset == 0 and y_offset == 0:
            continue
        yield Point(p.x + x_offset, p.y + y_offset)


def is_symbol(c) -> bool:
    return not c.isdigit() and c != "."


# Parse grid
grid = {}
ans = 0
for y, line in enumerate(data):
    for x, c in enumerate(line):
        grid[Point(x, y)] = c

# Find part numbers
pnv = ""
pns, symbol_pos = [], []
start, last_key = Point(0, 0), Point(0, 0)
for k, v in grid.items():
    if v.isdigit():
        pnv += v
        if len(pnv) == 1:
            start = k
    else:
        if is_symbol(v):
            symbol_pos.append(k)
        if len(pnv) > 0:
            pns.append(PartNumber(int(pnv), start, last_key))
        pnv = ""
        start = None
    last_key = k

# Part 1 and 2 solution
part_numbers = set()
ans2 = 0
for k in symbol_pos:
    v = grid[k]
    ipns = set()
    is_gear_symbol = v == "*"
    for a in adjacent8(k):
        if a in grid and grid[a].isdigit():
            for pn in pns:
                if (pn.start == a or pn.stop == a) and pn not in part_numbers:
                    if is_gear_symbol:
                        ipns.add(pn)
                    part_numbers.add(pn)
    if len(ipns) == 2:
        gear_ratio = math.prod(pn.value for pn in ipns)
        ans2 += gear_ratio

print(f"Part 1: {sum(pn.value for pn in part_numbers)}")
print(f"Part 2: {ans2}")
