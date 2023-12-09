import sys
from collections import namedtuple

from rich import print

with open(sys.argv[1]) as f:
    data = f.read().strip().split("\n\n")

seeds = [int(x) for x in data[0].split(": ")[1].split()]
Map = namedtuple("Map", ["id", "maps"])
maps = []
for i, m in enumerate(data[1:]):
    _, *ms = m.split("\n")
    imap = []
    for m in ms:
        m = m.split()
        imap.append([int(x) for x in m])
    current_map = Map(i, imap)
    maps.append(current_map)


def apply_map(m: list[int], seed: int) -> int:
    dst_range_start, src_range_start, range_length = m
    if seed < src_range_start or seed > src_range_start + range_length:
        return seed
    src_range = range(src_range_start, src_range_start + range_length + 1)
    dst_range = range(dst_range_start, dst_range_start + range_length + 1)
    return dst_range[seed - src_range.start]


def forward_pass(seeds: list[int], m: Map) -> list[int]:
    tseeds = []
    for seed in seeds:
        original_seed = seed
        for im in m.maps:
            seed = apply_map(im, seed)
            if seed != original_seed:
                tseeds.append(seed)
                break
        if seed == original_seed:
            tseeds.append(seed)
    return tseeds


inputs = seeds
for m in maps:
    inputs = forward_pass(inputs, m)

print(f"Part 1: {min(inputs)}")

# Part 2

ranges = [range(e, e + length) for e, length in zip(seeds[::2], seeds[1::2])]


def objective(trial, irange):
    seed_candidate = trial.suggest_int("seed_candidate", ranges[irange].start, 2_000_000_000)
    test = [seed_candidate]
    for m in maps:
        test = forward_pass(test, m)
    return min(test)


# Brute force
# mins = {}
##for i in range(len(ranges)):
# study: Study = optuna.create_study(direction="minimize")
# study.optimize(lambda trial: objective(trial,2), n_trials=20_000, show_progress_bar=True)
# mins[2] = study.best_value
# print(f"{study.best_params=} {study.best_value=}")
# print(f"Part 2: {min(mins.values())}")
