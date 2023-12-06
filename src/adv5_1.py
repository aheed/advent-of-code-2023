from dataclasses import dataclass
import utils

@dataclass
class MapRange:
    dst_start: int
    src_start: int
    length: int

@dataclass
class Map:
    ranges: list[MapRange]

def range_get(rng: MapRange, input: int) -> int | None:
    if input >= rng.src_start and input < rng.src_start + rng.length:
        return input + rng.dst_start - rng.src_start
    return None

def map_get(map: Map, input: int) -> int:
    return next((output for rng in map.ranges if (output := range_get(rng=rng, input=input))), input)

def seed_to_location(seed: int, maps: list[Map]):
    tmp = seed
    for map in maps:
        tmp = map_get(map=map, input=tmp)
    return tmp

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

seeds : list[int] = []
maps: list[Map] = []
map_index = -1

for line in lines:
    if "seeds:" in line:
        seeds = [int(s) for s in line.split(": ")[1].split(" ")]
        #print(seeds)
        continue

    if ":" in line:
        map_index = map_index + 1
        maps.append(Map(ranges=[]))
        #print("new map", line)
        continue

    if len(line) == 0:
        #print("empty line")
        continue

    numbers = [int(n) for n in line.split(" ")]
    new_range = MapRange(dst_start=numbers[0], src_start=numbers[1], length=numbers[2])
    maps[map_index].ranges.append(new_range)

#print(maps)
locations = [seed_to_location(seed=seed, maps=maps) for seed in seeds]
print(min(locations))
