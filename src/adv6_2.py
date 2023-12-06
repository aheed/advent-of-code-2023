from dataclasses import dataclass
import math
import utils

@dataclass
class Race:
    time: int
    distance: int

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]


def get_numbers(line: str) -> list[int]:
    num_strs = line.split(": ")[1].split(" ")
    return [int(num_str) for num_str in num_strs if len(num_str) > 0]

times = get_numbers(lines[0])
distances = get_numbers(lines[1])

#print(times)
#print(distances)
#races = [Race(time=times[i], distance=distances[i]) for i in range(len(times))]
#races = [Race(time=71530, distance=940200)] #ex
races = [Race(time=53837288, distance=333163512891532)]
print(races)


def ways_to_win_race(race: Race) -> int:
    wins = 0
    for press_time in range(race.time+1):
        dist = press_time * (race.time - press_time)
        #print(dist)
        if dist > race.distance:
            wins = wins + 1
    return wins

print(math.prod([ways_to_win_race(race=race) for race in races]))
