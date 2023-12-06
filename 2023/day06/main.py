import sys
from dataclasses import dataclass

with open(sys.argv[1]) as f:
    data = f.read().strip().splitlines()


@dataclass(frozen=True)
class Race:
    time_last: int
    record_distance: int


def parse_races(data: list[str]) -> list[Race]:
    time, distance = data
    times = [int(t) for t in time.split(":")[1].split()]
    distances = [int(d) for d in distance.split(":")[1].split()]
    return [Race(t, d) for t, d in zip(times, distances)]


ans = 0
races = parse_races(data)


def explore_race_options(r: Race) -> int:
    record = r.record_distance
    budget = r.time_last
    num_ways = 0
    for i in range(budget):
        if i == 0:
            continue
        duration = budget - i
        speed = i
        distance = speed * duration
        if distance > record:
            num_ways += 1
    return num_ways


ans = 1
for r in races:
    ans *= explore_race_options(r)

print(ans)
