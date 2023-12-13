import sys

with open(sys.argv[1]) as f:
    data = f.read().strip()

patterns = data.split("\n\n")

ans = 0
for pattern in patterns:
    grid = {}

    pattern_lines = pattern.splitlines()
    for y, line in enumerate(pattern_lines):
        for x, c in enumerate(line):
            grid[(x, y)] = c

    n = len(pattern_lines)
    r = len(pattern_lines[0])
    for i in range(r - 1):
        c = 0
        for j in range(r):
            left = i - j
            right = i + 1 + j
            if 0 <= left < right < r:
                for k in range(n):
                    if grid[(left, k)] != grid[(right, k)]:
                        c += 1
        if c == 1:
            ans += i + 1

    for m in range(n - 1):
        c = 0
        for l in range(n):
            up = m - l
            down = m + 1 + l
            if 0 <= up < down < n:
                for o in range(r):
                    if grid[(o, up)] != grid[(o, down)]:
                        c += 1
        if c == 1:
            ans += 100 * (m + 1)

print(f"Part 2: {ans}")
