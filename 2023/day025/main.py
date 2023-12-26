import math
import random
import sys

import networkx as nx

with open(sys.argv[1]) as f:
    data = f.read().splitlines()

G = nx.Graph()
for line in data:
    src, dst = line.split(":")
    for d in dst.strip().split():
        G.add_edge(src, d, capacity=1)  # capacity=1 how much flow can go through this edge

# nx.nx_pydot.write_dot(G, "graph.dot")
cut_value = sys.maxsize
nodes = list(G.nodes)
partition = []
while cut_value > 3:
    n1 = random.choice(nodes)
    n2 = random.choice(nodes)
    cut_value, partition = nx.minimum_cut(G, n1, n2)

print(f"Part 1: {math.prod(len(p) for p in partition)}")
