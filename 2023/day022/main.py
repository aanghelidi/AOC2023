import itertools
import re
import sys
from typing import Iterable, NamedTuple

with open(sys.argv[1]) as f:
    data = f.read().splitlines()


class Point3D(NamedTuple):
    x: int
    y: int
    z: int


class Brick(NamedTuple):
    id: int
    points: list[Point3D]
    min_z: int


def parse_input(data: list[str]) -> list[Brick]:
    bricks = []
    nums = re.compile(r"-?\d+")
    for i, line in enumerate(data):
        x1, y1, z1, x2, y2, z2 = (int(x) for x in re.findall(nums, line))
        points = []
        min_z = sys.maxsize
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    points.append(Point3D(x, y, z))
                    min_z = min(min_z, z)
        bricks.append(Brick(i, points, min_z))
    return sorted(bricks, key=lambda x: x.min_z)


def lower_brick(b: Brick) -> Brick:
    return Brick(b.id, [Point3D(x, y, z - 1) for x, y, z in b.points], b.min_z - 1)


def can_lower(b: Brick, taken: set[tuple[int, int, int]]) -> bool:
    return b.min_z > 1 and not taken & {(x, y, z - 1) for x, y, z in b.points}


def fall_down(bricks: Iterable[Brick]) -> dict[int, Brick]:
    new_bricks = {}
    taken = set()
    for b in bricks:
        while can_lower(b, taken):
            b = lower_brick(b)
        taken |= set(b.points)
        new_bricks[b.id] = b
    return new_bricks


sorted_bricks = parse_input(data)
down_bricks = fall_down(sorted_bricks)
ans = 0
ans2 = 0
for pblocks in itertools.combinations(down_bricks.values(), len(down_bricks) - 1):
    pblocks = fall_down(pblocks)
    ans += all(b.min_z == down_bricks[id].min_z for id, b in pblocks.items())
    ans2 += sum(b.min_z != down_bricks[id].min_z for id, b in pblocks.items())

print(f"Part 1: {ans}")
print(f"Part 2: {ans2}")
