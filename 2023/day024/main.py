import itertools
import sys
from typing import NamedTuple

with open(sys.argv[1]) as f:
    data = f.read().splitlines()


class Position(NamedTuple):
    x: int
    y: int
    z: int


class Velocity(NamedTuple):
    x: int
    y: int
    z: int


class Hailstone(NamedTuple):
    initial_position: Position
    velocity: Velocity


hailstones: list[Hailstone] = []
for line in data:
    positions, _, velocities = line.partition(" @ ")
    px, py, pz = (int(x) for x in positions.strip().split(","))
    vx, vy, vz = (int(x) for x in velocities.strip().split(","))
    hailstones.append(Hailstone(Position(px, py, pz), Velocity(vx, vy, vz)))

ans = 0
LOW = 200000000000000
HIGH = 400000000000000
for hs, hs2 in itertools.combinations(hailstones, 2):
    a1, b1, c1 = (
        hs.velocity.y,
        -hs.velocity.x,
        (hs.velocity.y * hs.initial_position.x) - (hs.velocity.x * hs.initial_position.y),
    )

    a2, b2, c2 = (
        hs2.velocity.y,
        -hs2.velocity.x,
        (hs2.velocity.y * hs2.initial_position.x) - (hs2.velocity.x * hs2.initial_position.y),
    )

    # Prevent division by zero
    if (d := (a1 * b2 - a2 * b1)) == 0:
        continue

    x = (b2 * c1 - b1 * c2) / d
    y = (a1 * c2 - a2 * c1) / d

    if LOW <= x <= HIGH and LOW <= y <= HIGH:
        if all(
            (x - hs.initial_position.x) * hs.velocity.x >= 0 and (y - hs.initial_position.y) * hs.velocity.y >= 0
            for hs in (hs, hs2)
        ):
            ans += 1

print(f"Part 1: {ans}")
