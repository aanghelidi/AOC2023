import sys
from typing import NamedTuple

from sympy import nonlinsolve, symbols

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

xpx, ypy, zpz, vvx, vvy, vvz = symbols("xpx, ypy, zpz, vvx, vvy, vvz")
eqns = []
for i, h in enumerate(hailstones):
    px, py, pz = h.initial_position
    vx, vy, vz = h.velocity
    eqns.append((xpx - px) * (vy - vvy) - (ypy - py) * (vx - vvx))
    eqns.append((ypy - py) * (vz - vvz) - (zpz - pz) * (vy - vvy))
    if i < 2:
        continue
    sset = nonlinsolve(eqns, [xpx, ypy, zpz, vvx, vvy, vvz])
    if len(sset) == 1:
        break

for x in sset:
    print(f"Part 2: {x[0] + x[1] + x[2]}")
