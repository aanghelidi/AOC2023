import sys
from itertools import pairwise

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

ans = 0
ans2 = 0
for i, line in enumerate(data):
    histories = []
    history = [int(n) for n in line.strip().split()]
    histories.append(history)
    while any(e != 0 for e in history):
        history = [b - a for a, b in pairwise(history)]
        histories.append(history)
    histories[-1].append(0)
    for i in range(len(histories) - 2, -1, -1):
        h = histories[i]
        prev_h = histories[i + 1]
        new_zero = prev_h[-1] + h[-1]
        new_zero_2 = h[0] - prev_h[0]
        h.append(new_zero)
        h.insert(0, new_zero_2)
    next_value = histories[0][-1]
    ans += next_value
    next_value_2 = histories[0][0]
    ans2 += next_value_2

print(f"Part 1: {ans}")
print(f"Part 2: {ans2}")
