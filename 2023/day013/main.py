import sys
from itertools import zip_longest
from typing import Literal

with open(sys.argv[1]) as f:
    data = f.read().strip()

patterns = data.split("\n\n")


def get_positions(pattern: str, type: Literal["rock", "ash"]) -> set[tuple[int, int]]:
    positions = set()
    all_positions = set()
    char = "#" if type == "rock" else "."
    for y, line in enumerate(pattern.splitlines()):
        for x, c in enumerate(line):
            all_positions.add((x, y))
            if c == "#":
                positions.add((x, y))
    return positions if char == "#" else all_positions - positions


def find_potential_v_reflection(pattern: str, positions: set[tuple[int, int]]) -> list[tuple[int, int]]:
    pattern_lines = pattern.splitlines()
    n = len(pattern_lines[0])
    p_reflections = []
    for x in range(n - 1):
        current_col = x
        next_col = x + 1
        rocks_in_current_col = {pos[1] for pos in positions if pos[0] == current_col}
        rocks_in_next_col = {pos[1] for pos in positions if pos[0] == next_col}
        if rocks_in_current_col == rocks_in_next_col:
            p_reflections.append((current_col, next_col))
    return p_reflections if p_reflections else [(-1, -1)]


def find_potential_h_reflection(pattern: str, positions: set[tuple[int, int]]) -> list[tuple[int, int]]:
    pattern_lines = pattern.splitlines()
    n = len(pattern_lines)
    p_reflections = []
    for y in range(n - 1):
        current_row = y
        next_row = y + 1
        rocks_in_current_row = {pos[0] for pos in positions if pos[1] == current_row}
        rocks_in_next_row = {pos[0] for pos in positions if pos[1] == next_row}
        if rocks_in_current_row == rocks_in_next_row:
            p_reflections.append((current_row, next_row))
    return p_reflections if p_reflections else [(-1, -1)]


def find_perfect_reflection_h(
    pattern: str,
    positions: set[tuple[int, int]],
    p_reflection: tuple[int, int],
) -> tuple[tuple[int, int], str, int]:
    pattern_lines = pattern.splitlines()
    n_rows_before_reflection = p_reflection[0] + 1
    n_rows_after_reflection = len(pattern_lines) - p_reflection[1]
    check_range = range(1, min(n_rows_before_reflection, n_rows_after_reflection))
    is_perfect = True
    for row in check_range:
        row_above = p_reflection[0] - row
        row_below = p_reflection[1] + row
        rocks_in_row_above = {pos[0] for pos in positions if pos[1] == row_above}
        rocks_in_row_below = {pos[0] for pos in positions if pos[1] == row_below}
        if rocks_in_row_above != rocks_in_row_below:
            is_perfect = False
            break
    if is_perfect:
        return p_reflection, "h", n_rows_before_reflection
    else:
        # no perfect reflection found
        return p_reflection, "x", 0


def find_perfect_reflection_v(
    pattern: str,
    positions: set[tuple[int, int]],
    p_reflection: tuple[int, int],
) -> tuple[tuple[int, int], str, int]:
    pattern_lines = pattern.splitlines()
    n_cols_before_reflection = p_reflection[0] + 1
    n_cols_after_reflection = len(pattern_lines[0]) - p_reflection[1]
    check_range = range(1, min(n_cols_before_reflection, n_cols_after_reflection))
    is_perfect = True
    for col in check_range:
        col_left = p_reflection[0] - col
        col_right = p_reflection[1] + col
        rocks_in_col_left = {pos[1] for pos in positions if pos[0] == col_left}
        rocks_in_col_right = {pos[1] for pos in positions if pos[0] == col_right}
        if rocks_in_col_left != rocks_in_col_right:
            is_perfect = False
            break
    if is_perfect:
        return p_reflection, "v", n_cols_before_reflection
    else:
        # no perfect reflection found
        return p_reflection, "x", 0


def score(nv: int, nh: int) -> int:
    return nv + (nh * 100)


if __name__ == "__main__":
    ans = 0
    for pattern in patterns:
        rock_positions = get_positions(pattern, "rock")
        p_h_reflection = find_potential_h_reflection(pattern, rock_positions)
        p_v_reflection = find_potential_v_reflection(pattern, rock_positions)
        nhs = []
        if nhs == [(-1, -1)]:
            nhs = [0]
        else:
            for ph in p_h_reflection:
                reflection, t, nh = find_perfect_reflection_h(pattern, rock_positions, ph)
                if t == "x":
                    continue
                nhs.append(nh)
        nvs = []
        if nvs == [(-1, -1)]:
            nvs = [0]
        else:
            for pv in p_v_reflection:
                reflection, t, nv = find_perfect_reflection_v(pattern, rock_positions, pv)
                if t == "x":
                    continue
                nvs.append(nv)
        for nv, nh in zip_longest(nvs, nhs, fillvalue=0):
            ans += score(nv, nh)
    print(f"Part 1: {ans}")
