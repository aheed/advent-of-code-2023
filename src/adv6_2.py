from dataclasses import dataclass
import math

@dataclass
class Race:
    time: int
    distance: int

races = [Race(time=53837288, distance=333163512891532)]
#print(races)

def ways_to_win_race(race: Race) -> int:
    wins = 0
    for press_time in range(race.time+1):
        dist = press_time * (race.time - press_time)
        if dist > race.distance:
            wins = wins + 1
    return wins

print(math.prod([ways_to_win_race(race=race) for race in races]))
