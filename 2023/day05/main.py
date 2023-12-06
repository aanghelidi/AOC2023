import sys
from dataclasses import dataclass
from itertools import pairwise
from typing import NamedTuple

with open(sys.argv[1]) as f:
    data = f.read()


class MapRange(NamedTuple):
    destination_range_start: int
    source_range_start: int
    range_length: int


@dataclass(frozen=True)
class ConversionMap:
    source_category: str
    destination_category: str
    maps: list[MapRange]

    @classmethod
    def parse(cls, s):
        source_category, destination_category = s.split("-to-")
        destination_category = destination_category.split(" ")[0]
        maps = []
        for line in s.split("\n")[1:]:
            destination_range_start, source_range_start, range_length = (int(x) for x in line.split(" "))
            maps.append(MapRange(destination_range_start, source_range_start, range_length))
        return cls(source_category, destination_category, maps)


ans = 0
seeds, *maps = data.strip().split("\n\n")
seeds = [int(x) for x in seeds.split(": ")[1].split(" ")]

cv_maps: list[ConversionMap] = []
for map in maps:
    conversion_map = ConversionMap.parse(map)
    cv_maps.append(conversion_map)


def convert_with_maps(c_from: str, c_to: str, cv_maps: list[ConversionMap], seeds: list[int]) -> list[int]:
    converted = set()
    conversion_dict = {}
    filtered_cv_maps = [
        cv_map for cv_map in cv_maps if cv_map.source_category == c_from and cv_map.destination_category == c_to
    ]
    for seed in seeds:
        for cv_map in filtered_cv_maps:
            for source_range_start, destination_range_start, range_length in cv_map.maps:
                if seed in range(destination_range_start, destination_range_start + range_length):
                    seed_converted = seed - destination_range_start + source_range_start
                    converted.add(seed)
                    conversion_dict[seed] = seed_converted
    remaining_seeds = set(seeds) - converted
    for seed in remaining_seeds:
        conversion_dict[seed] = seed
    return [conversion_dict[seed] for seed in seeds]


soils = convert_with_maps("seed", "soil", cv_maps, seeds)
fertilizers = convert_with_maps("soil", "fertilizer", cv_maps, soils)
waters = convert_with_maps("fertilizer", "water", cv_maps, fertilizers)
lights = convert_with_maps("water", "light", cv_maps, waters)
temperatures = convert_with_maps("light", "temperature", cv_maps, lights)
humidities = convert_with_maps("temperature", "humidity", cv_maps, temperatures)
locations = convert_with_maps("humidity", "location", cv_maps, humidities)

print(f"Part 1: {min(locations)}")

# Part 2
ranges = [range(s1, s1 + s2) for idx, (s1, s2) in enumerate(pairwise(seeds)) if idx % 2 == 0]

# def f(seeds):
#    soils = convert_with_maps("seed", "soil", cv_maps, seeds)
#    fertilizers = convert_with_maps("soil", "fertilizer", cv_maps, soils)
#    waters = convert_with_maps("fertilizer", "water", cv_maps, fertilizers)
#    lights = convert_with_maps("water", "light", cv_maps, waters)
#    temperatures = convert_with_maps("light", "temperature", cv_maps, lights)
#    humidities = convert_with_maps("temperature", "humidity", cv_maps, temperatures)
#    locations = convert_with_maps("humidity", "location", cv_maps, humidities)
#    return min(locations)
#
# with mp.Pool(20) as p:
#    print(f"Part 2: {min(p.map(f, ranges,chunksize=1024))}")
