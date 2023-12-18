import sys

from shapely.geometry import Polygon

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

ans = 0
current = complex(0, 0)
visited: list[complex] = []
visited.append(current)
dmap = dict(zip("0123", "RDLU"))
for part in (1, 2):
    for line in data:
        dir, m, rgb = line.strip().split()
        m = int(m)
        rgb = rgb.removeprefix("(").removesuffix(")").removeprefix("#")
        if part == 2:
            m = int(rgb[:5], 16)
            dir = dmap[rgb[-1]]
        if dir == "R":
            current += complex(1, 0) * m
            visited.append(current)
        elif dir == "D":
            current += complex(0, 1) * m
            visited.append(current)
        elif dir == "L":
            current += complex(-1, 0) * m
            visited.append(current)
        elif dir == "U":
            current += complex(0, -1) * m
            visited.append(current)

    coords = [(z.real, z.imag) for z in visited]
    polygon = Polygon(coords)
    ans = int(polygon.area + polygon.length / 2 + 1)
    print(f"Part {part}: {ans}")
