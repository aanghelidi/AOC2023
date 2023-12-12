import sys
from functools import lru_cache

with open(sys.argv[1]) as f:
    data = f.read().splitlines()


@lru_cache(maxsize=None)
def count_arrangements(
    spring_row: str, groups_info: tuple[int], position: int = 0, current_count: int = 0, position_count: int = 0
) -> int:
    n = len(spring_row)
    k = len(groups_info)
    if position == n:
        return 1 if k == position_count else 0
    elif spring_row[position] == "." or position_count == k:
        if position_count < k and current_count == groups_info[position_count]:
            return count_arrangements(spring_row, groups_info, position + 1, 0, position_count + 1)
        elif current_count == 0:
            return count_arrangements(spring_row, groups_info, position + 1, 0, position_count)
        else:
            return 0
    elif spring_row[position] == "#":
        return count_arrangements(spring_row, groups_info, position + 1, current_count + 1, position_count)
    else:
        hash_count = count_arrangements(spring_row, groups_info, position + 1, current_count + 1, position_count)
        dot_count = 0
        if current_count == groups_info[position_count]:
            dot_count = count_arrangements(spring_row, groups_info, position + 1, 0, position_count + 1)
        elif current_count == 0:
            dot_count = count_arrangements(spring_row, groups_info, position + 1, 0, position_count)
        return hash_count + dot_count


ans = 0
for line in data:
    spring_row, groups_info = line.strip().split()
    spring_row += "."
    groups_info = tuple([int(x) for x in groups_info.strip().split(",")])
    ans += count_arrangements(spring_row, groups_info)
print(f"Part 1: {ans}")

ans2 = 0
for line in data:
    spring_row, groups_info = line.strip().split()
    spring_row = [spring_row] * 5
    spring_row = "?".join(spring_row)
    spring_row += "."
    groups_info = tuple([int(x) for x in groups_info.strip().split(",")] * 5)
    ans2 += count_arrangements(spring_row, groups_info)
print(f"Part 2: {ans2}")
