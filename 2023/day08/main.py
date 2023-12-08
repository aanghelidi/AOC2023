import itertools
import sys
from collections import defaultdict
from math import lcm

with open(sys.argv[1]) as f:
    data = f.read().strip()

instructions, *rest = data.split("\n\n")
graph = defaultdict(list)

for element in rest[0].split("\n"):
    node, *dests = element.split(" = ")
    left, right = dests[0].removeprefix("(").removesuffix(")").split(", ")
    graph[node] = [left, right]

start = current_node = "AAA"
ans = 0
for i in itertools.cycle(instructions):
    if i == "L":
        current_node = graph[current_node][0]
    else:
        current_node = graph[current_node][1]
    ans += 1
    if current_node == "ZZZ":
        break

print(f"Part 1: {ans}")

starts = [k for k in graph if k.endswith("A")]
steps_counter = {}
for i, current_node in enumerate(starts):
    count = 0
    for i in itertools.cycle(instructions):
        if i == "L":
            current_node = graph[current_node][0]
        else:
            current_node = graph[current_node][1]
        count += 1
        if current_node.endswith("Z"):
            steps_counter[current_node] = count
            break

print(f"Part 2: {lcm(*steps_counter.values())}")
