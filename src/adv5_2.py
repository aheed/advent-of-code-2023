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

big_number = 100000000000

def range_get(rng: MapRange, input: int) -> int | None:
    if input >= rng.src_start and input < rng.src_start + rng.length:
        return input + rng.dst_start - rng.src_start
    return None

def range_get_max_increment(rng: MapRange, input: int) -> int:
    if input >= rng.src_start and input < rng.src_start + rng.length:
        return rng.src_start + rng.length - input
    return big_number

def map_get(map: Map, input: int) -> int:
    return next((output for rng in map.ranges if (output := range_get(rng=rng, input=input))), input)

def map_get_max_increment(map: Map, input: int) -> int:
    return min([range_get_max_increment(rng=rng, input=input) for rng in map.ranges])

def seed_to_location(seed: int, maps: list[Map]):
    if seed % 10000 == 0:
        print(".")
    tmp = seed
    for map in maps:
        tmp = map_get(map=map, input=tmp)
    return tmp

def seed_to_max_increment(seed: int, maps: list[Map]):
    ret = big_number
    tmp = seed
    for map in maps:
        ret = min(ret, map_get_max_increment(map=map, input=tmp))
        tmp = map_get(map=map, input=tmp)
    return ret

def seed_range_to_min_location(range_start: int, range_length: int, maps: list[Map]):
    min_location = big_number
    candidate_seed = range_start
    while candidate_seed < range_start + range_length:
        min_location = min(min_location, seed_to_location(seed=candidate_seed, maps=maps))
        candidate_seed = candidate_seed + seed_to_max_increment(seed=candidate_seed, maps=maps)
    return min_location

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

seeds : list[int] = []
maps: list[Map] = []
map_index = -1

for line in lines:
    if "seeds:" in line:
        seeds = [int(s) for s in line.split(": ")[1].split(" ")]
        continue

    if ":" in line:
        map_index = map_index + 1
        maps.append(Map(ranges=[]))
        continue

    if len(line) == 0:
        continue

    numbers = [int(n) for n in line.split(" ")]
    new_range = MapRange(dst_start=numbers[0], src_start=numbers[1], length=numbers[2])
    maps[map_index].ranges.append(new_range)

m = [seed_range_to_min_location(range_start=seeds[i], range_length=seeds[i+1], maps=maps) for i in range(0, len(seeds), 2)]
#print(m)
print(min(m))