import itertools
import sys

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

image = {}
for y, row in enumerate(data):
    for x, pixel in enumerate(row):
        image[(x, y)] = pixel


def display_image(image: dict) -> None:
    max_x, max_y = max(image)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(image[(x, y)], end="")
        print("")


def is_galaxy(s: str) -> bool:
    return s == "#"


def detect_columns_with_no_galaxies(image: dict) -> list[int]:
    columns_with_no_galaxies = []
    max_x, max_y = max(image)
    for x in range(max_x + 1):
        column_has_galaxy = False
        for y in range(max_y + 1):
            if is_galaxy(image[(x, y)]):
                column_has_galaxy = True
                break
        if not column_has_galaxy:
            columns_with_no_galaxies.append(x)
    return columns_with_no_galaxies


def detect_rows_with_no_galaxies(image: dict) -> list[int]:
    rows_with_no_galaxies = []
    max_x, max_y = max(image)
    for y in range(max_y + 1):
        row_has_galaxy = False
        for x in range(max_x + 1):
            if is_galaxy(image[(x, y)]):
                row_has_galaxy = True
                break
        if not row_has_galaxy:
            rows_with_no_galaxies.append(y)
    return rows_with_no_galaxies


def turn_galaxy_to_number(image: dict) -> tuple[dict, dict]:
    new_image = {}
    galaxies_positions = {}
    current_number = 1
    max_x, max_y = max(image)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if is_galaxy(image[(x, y)]):
                new_image[(x, y)] = str(current_number)
                galaxies_positions[current_number] = (x, y)
                current_number += 1
            else:
                new_image[(x, y)] = image[(x, y)]
    return new_image, galaxies_positions


def convert_gpos_with_offset(
    gpos: tuple[int, int], columns: list[int], rows: list[int], factor: int
) -> tuple[int, int]:
    x, y = gpos
    dx = sum(x > e for e in columns)
    dy = sum(y > e for e in rows)
    new_x = x + (dx * factor) - dx
    new_y = y + (dy * factor) - dy
    return (new_x, new_y)


def manhattan_between_galaxies(galaxies_positions: dict, pair_of_galaxies: tuple[int, int]) -> int:
    start = galaxies_positions[pair_of_galaxies[0]]
    end = galaxies_positions[pair_of_galaxies[1]]
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


columns = detect_columns_with_no_galaxies(image)
rows = detect_rows_with_no_galaxies(image)
image_dbg, galaxies_positions_origin = turn_galaxy_to_number(image)

for part, duplicate_factor in zip((1, 2), (2, 1_000_000)):
    galaxies_positions = {
        k: convert_gpos_with_offset(v, columns, rows, duplicate_factor) for k, v in galaxies_positions_origin.items()
    }
    number_of_galaxies = len(galaxies_positions)
    it = range(1, number_of_galaxies + 1)
    combinations = itertools.combinations(it, 2)
    ans = 0
    for pair in combinations:
        ans += manhattan_between_galaxies(galaxies_positions, pair)
    print(f"Part {part}:", ans)
