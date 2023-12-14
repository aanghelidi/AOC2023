import sys
from collections import deque
from functools import cache
from typing import Generator, Literal

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

grid = {}

for y, line in enumerate(data):
    for x, char in enumerate(line):
        grid[complex(x, y)] = char


def north(pos: complex) -> Generator[complex, None, None]:
    yield pos - 1j


def south(pos: complex) -> Generator[complex, None, None]:
    yield pos + 1j


def east(pos: complex) -> Generator[complex, None, None]:
    yield pos + 1


def west(pos: complex) -> Generator[complex, None, None]:
    yield pos - 1


Direction = Literal["north", "east", "south", "west"]


@cache
def tilting(grid_keys: tuple[complex], grid_values: tuple[str], direction: Direction) -> dict[complex, str]:
    grid = dict(zip(grid_keys, grid_values))
    rounded_rocks = deque()
    for pos in grid:
        if grid[pos] == "O":
            rounded_rocks.append(pos)
    if direction == "north":
        while rounded_rocks:
            rock = rounded_rocks.popleft()
            stop = False
            while not stop:
                previous_rock = rock
                rock = next(north(rock))
                if rock in grid:
                    if grid[rock] == "#" or grid[rock] == "O":
                        stop = True
                    else:
                        grid[previous_rock] = "."
                        grid[rock] = "O"
                else:
                    stop = True
    elif direction == "south":
        while rounded_rocks:
            rock = rounded_rocks.pop()
            stop = False
            while not stop:
                previous_rock = rock
                rock = next(south(rock))
                if rock in grid:
                    if grid[rock] == "#" or grid[rock] == "O":
                        stop = True
                    else:
                        grid[previous_rock] = "."
                        grid[rock] = "O"
                else:
                    stop = True
    elif direction == "east":
        rotated_grid = {}
        for pos in grid:
            new_pos = pos * 1j
            rotated_grid[new_pos] = grid[pos]
        rotated_tilted_grid = tilting(tuple(rotated_grid.keys()), (rotated_grid.values()), "south")
        final_grid = {}
        for pos in rotated_tilted_grid:
            new_pos = pos * -1j
            final_grid[new_pos] = rotated_tilted_grid[pos]
        return final_grid
    elif direction == "west":
        rotated_grid = {}
        for pos in grid:
            new_pos = pos * 1j
            rotated_grid[new_pos] = grid[pos]
        rotated_tilted_grid = tilting(tuple(rotated_grid.keys()), tuple(rotated_grid.values()), "north")
        final_grid = {}
        for pos in rotated_tilted_grid:
            new_pos = pos * -1j
            final_grid[new_pos] = rotated_tilted_grid[pos]
        return final_grid
    else:
        raise ValueError(f"Invalid direction: {direction}")
    return grid


def cycle(grid: dict[complex, str]) -> dict[complex, str]:
    first = tilting(tuple(grid.keys()), tuple(grid.values()), "north")
    second = tilting(tuple(first.keys()), tuple(first.values()), "west")
    third = tilting(tuple(second.keys()), tuple(second.values()), "south")
    fourth = tilting(tuple(third.keys()), tuple(third.values()), "east")
    return fourth


def total_load(grid: dict[complex, str]) -> int:
    max_y = int(max(grid, key=lambda x: x.imag).imag)
    max_x = int(max(grid, key=lambda x: x.real).real)
    total_load = 0
    factor = 1
    for y in range(max_y, -1, -1):
        for x in range(max_x + 1):
            if grid[complex(x, y)] == "O":
                total_load += factor
        factor += 1
    return total_load


# Part 1
# tilting all the rocks to the north
# grid = tilting(tuple(grid.keys()), tuple(grid.values()), "north")
# print(f"Part 1: {total_load(grid)}")

# Part 2
cycles = 1_000_000_000
current_cycle = 0
history = {}
while current_cycle < cycles:
    current_cycle += 1
    grid = cycle(grid)
    state = str(grid)
    if state in history:
        cycle_length = current_cycle - history[state]
        factor = (cycles - current_cycle) // cycle_length
        # fast foward
        current_cycle += cycle_length * factor
    history[state] = current_cycle

print(f"Part 2: {total_load(grid)}")
