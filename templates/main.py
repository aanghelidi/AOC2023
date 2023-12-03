import sys

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

ans = 0
for line in data:
    print(line)
