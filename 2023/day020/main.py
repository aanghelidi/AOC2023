import sys
from collections import deque

import networkx as nx

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

G = nx.DiGraph(name="Circuit")
flipflops = set()
conjunctions = set()
for line in data:
    src, dst = line.split(" -> ")
    src = src.strip()
    for d in dst.strip().split(","):
        d = d.strip()
        if src.startswith("%"):
            src = src.removeprefix("%")
            G.add_edge(src, d)
            flipflops.add(src)
        elif src.startswith("&"):
            src = src.removeprefix("&")
            G.add_edge(src, d)
            conjunctions.add(src)
        else:
            G.add_edge(src, d)

nx.nx_pydot.write_dot(G, "graph.dot")

flipflops_states = {e: 0 for e in flipflops}
mem_conjunctions = {}

for c in conjunctions:
    inputs = list(G.predecessors(c))
    for i in inputs:
        if mem_conjunctions.get(c) is None:
            mem_conjunctions[c] = {}
        mem_conjunctions[c][i] = 0

cycle = 0
low_pulse = 0
high_pulse = 0
while cycle < 1000:
    cycle += 1
    # print("")
    # print(f"Cycle {cycle}")
    Q = deque([("button", 0)])
    while Q:
        src, pulse = Q.popleft()
        if src == "button":
            # print(f"button -{pulse}-> broadcaster")
            if pulse == 0:
                low_pulse += 1
            elif pulse == 1:
                high_pulse += 1
            Q.append(("broadcaster", 0))
            continue
        if src in flipflops and pulse == 0:
            # low pulse, flips between 0 and 1
            flipflops_states[src] = 1 if flipflops_states[src] == 0 else 0
        for dst in G.successors(src):
            if src == "broadcaster":
                # print(f"broadcaster -{pulse}-> {dst}")
                if pulse == 0:
                    low_pulse += 1
                elif pulse == 1:
                    high_pulse += 1
                Q.append((dst, pulse))
            elif src in flipflops:
                if pulse == 0:
                    # print(f"{src} -{flipflops_states[src]}-> {dst}")
                    if flipflops_states[src] == 0:
                        low_pulse += 1
                    elif flipflops_states[src] == 1:
                        high_pulse += 1
                    Q.append((dst, flipflops_states[src]))
            elif src in conjunctions:
                # update mem conjunctions with flipflop states
                for fs in flipflops_states:
                    for m in mem_conjunctions:
                        if fs in mem_conjunctions[m]:
                            mem_conjunctions[m][fs] = flipflops_states[fs]
                if all(mem_conjunctions[src].values()):
                    pulse = 0 if pulse == 1 else 1
                else:
                    pulse = 1
                if pulse == 0:
                    low_pulse += 1
                elif pulse == 1:
                    high_pulse += 1
                # print(f"{src} -{pulse}-> {dst}")
                Q.append((dst, pulse))

print(f"Part 1: {high_pulse * low_pulse}")
