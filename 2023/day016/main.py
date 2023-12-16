import sys
from collections import deque
from copy import deepcopy
from typing import NamedTuple

with open(sys.argv[1]) as f:
    data = f.read().splitlines()


def gdisplay(g: dict[complex, str]) -> None:
    max_x = max(int(c.real) for c in g.keys())
    max_y = max(int(c.imag) for c in g.keys())
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(g[complex(x, y)], end="")
        print()


class Beam(NamedTuple):
    position: complex
    heading: complex


grid = {}
for y, line in enumerate(data):
    for x, c in enumerate(line):
        grid[complex(x, y)] = c


def correct_start(start: Beam, grid: dict[complex, str]) -> list[Beam]:
    mx = max(int(c.real) for c in grid.keys())
    my = max(int(c.imag) for c in grid.keys())
    if start.position == complex(0, 0):
        start2 = Beam(complex(start.position), complex(0, 1))
        return [start, start2]
    elif start.position == complex(0, my):
        start2 = Beam(complex(start.position), complex(0, -1))
        return [start, start2]
    elif start.position == complex(mx, 0):
        start2 = Beam(complex(start.position), complex(0, 1))
        return [start, start2]
    elif start.position == complex(mx, my):
        start2 = Beam(complex(start.position), complex(0, -1))
        return [start, start2]
    else:
        if start.position.real == 0:
            if grid[start.position] == "|":
                start = Beam(start.position, complex(0, 1))
                start2 = Beam(start.position, complex(0, -1))
                return [start, start2]
            elif grid[start.position] == "\\":
                start = Beam(start.position, complex(0, 1))
                return [start]
            elif grid[start.position] == "/":
                start = Beam(start.position, complex(0, -1))
                return [start]
            else:
                return [start]
        elif start.position.real == mx:
            if grid[start.position] == "|":
                start = Beam(start.position, complex(0, 1))
                start2 = Beam(start.position, complex(0, -1))
                return [start, start2]
            elif grid[start.position] == "\\":
                start = Beam(start.position, complex(0, -1))
                return [start]
            elif grid[start.position] == "/":
                start = Beam(start.position, complex(0, 1))
                return [start]
            else:
                return [start]
        elif start.position.imag == 0:
            if grid[start.position] == "-":
                start = Beam(start.position, complex(1, 0))
                start2 = Beam(start.position, complex(-1, 0))
                return [start, start2]
            elif grid[start.position] == "\\":
                start = Beam(start.position, complex(1, 0))
                return [start]
            elif grid[start.position] == "/":
                start = Beam(start.position, complex(-1, 0))
                return [start]
            else:
                return [start]
        elif start.position.imag == my:
            if grid[start.position] == "-":
                start = Beam(start.position, complex(1, 0))
                start2 = Beam(start.position, complex(-1, 0))
                return [start, start2]
            elif grid[start.position] == "\\":
                start = Beam(start.position, complex(-1, 0))
                return [start]
            elif grid[start.position] == "/":
                start = Beam(start.position, complex(1, 0))
                return [start]
            else:
                return [start]
        else:
            raise ValueError(f"Invalide start position {start.position}")


def tiles_energized(grid: dict[complex, str], part: int, start: Beam) -> int:
    db = deepcopy(grid)
    if part == 1:
        if grid[start.position] == "|" or grid[start.position] == "\\":
            start = Beam(complex(0, 0), complex(0, 1))
        beams = deque([start])
        visited = set()
        visited.add(start)
    else:
        beams = deque([start])
        visited = set()
        visited.add(start)
    while beams:
        pos, heading = beams.popleft()
        next_pos = pos + heading
        if next_pos not in grid or next_pos in visited:
            continue
        db[next_pos] = "#"
        if grid[next_pos] == ".":
            beams.append(Beam(next_pos, heading))
            visited.add(Beam(next_pos, heading))
        elif grid[next_pos] in ("/", "\\"):
            tile = grid[next_pos]
            if tile == "/":
                if heading == complex(1, 0) or heading == complex(-1, 0):
                    new_heading = heading * complex(0, -1)
                    if (beam := Beam(next_pos, new_heading)) not in visited:
                        beams.append(beam)
                        visited.add(beam)
                else:
                    new_heading = heading * complex(0, 1)
                    if (beam := Beam(next_pos, new_heading)) not in visited:
                        beams.append(beam)
                        visited.add(beam)
            else:
                if heading == complex(1, 0) or heading == complex(-1, 0):
                    new_heading = heading * complex(0, 1)
                    if (beam := Beam(next_pos, new_heading)) not in visited:
                        beams.append(beam)
                        visited.add(beam)
                else:
                    new_heading = heading * complex(0, -1)
                    if (beam := Beam(next_pos, new_heading)) not in visited:
                        beams.append(beam)
                        visited.add(beam)
        elif grid[next_pos] in ("|", "-"):
            tile = grid[next_pos]
            if tile == "|":
                if heading == complex(0, 1) or heading == complex(0, -1):
                    if (beam := Beam(next_pos, heading)) not in visited:
                        beams.append(beam)
                        visited.add(beam)
                else:
                    if (beam := Beam(next_pos, heading * complex(0, -1))) not in visited:
                        beams.append(beam)
                        visited.add(beam)
                    if (beam := Beam(next_pos, heading * complex(0, 1))) not in visited:
                        beams.append(beam)
                        visited.add(beam)
            else:
                if heading == complex(1, 0) or heading == complex(-1, 0):
                    if (beam := Beam(next_pos, heading)) not in visited:
                        beams.append(beam)
                        visited.add(beam)
                else:
                    if (beam := Beam(next_pos, heading * complex(0, -1))) not in visited:
                        beams.append(beam)
                        visited.add(beam)
                    if (beam := Beam(next_pos, heading * complex(0, 1))) not in visited:
                        beams.append(beam)
                        visited.add(beam)
        else:
            raise ValueError(f"Unknown tile {tile}")
    return sum(v == "#" for v in db.values()) + 1


print(f"Part 1: {tiles_energized(grid, 1, Beam(complex(0, 0), complex(1, 0)))}")

start_positions = []
max_x = max(int(c.real) for c in grid.keys())
max_y = max(int(c.imag) for c in grid.keys())
for y in range(max_y + 1):
    for x in range(max_x + 1):
        if x == 0 or x == max_x or y == 0 or y == max_y:
            start_positions.append(complex(x, y))

beam_starts = []
for s in start_positions:
    if s.real == 0:
        beam_starts.append(Beam(s, complex(1, 0)))
    elif s.real == max_x:
        beam_starts.append(Beam(s, complex(-1, 0)))
    elif s.imag == 0:
        beam_starts.append(Beam(s, complex(0, 1)))
    elif s.imag == max_y:
        beam_starts.append(Beam(s, complex(0, -1)))
    else:
        continue


corrected_starts = []
for s in beam_starts:
    corrected_starts.extend(correct_start(s, grid))


energies = []
for s in corrected_starts:
    energies.append(tiles_energized(grid, 2, s))

print(f"Part 2: {max(energies)}")
