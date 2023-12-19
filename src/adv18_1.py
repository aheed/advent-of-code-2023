from enum import Enum
from dataclasses import dataclass
import utils

@dataclass(frozen=True)
class Instruction:
    direction: str
    distance: int
    color: int

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

def get_instruction(line: str) -> Instruction:
    parts = line.split(" ")
    return Instruction(direction=parts[0], distance=int(parts[1]), color=int(parts[2][2:-1], 16))

instructions = [get_instruction(line) for line in lines]
print(instructions)

# (list of path tiles (holes))
  # just iterate the path and keep track of x and y to get max values
# create grid of tiles, dimensions given by max x,y in path tile collection
# set correct status on all path tiles (second iteration) and Inside and Outside status
# iterate until there are no Unknown tiles as in adv10_2
# Result = sum(path tiles) + sum(Inside tiles)

x=0
y=0
min_x = x
min_y = y
max_x = x
max_y = y
for instr in instructions:
    match instr.direction:
        case "R":
            x = x + instr.distance
        case "L":
            x = x - instr.distance
        case "D":
            y = y + instr.distance
        case "U":
            y = y - instr.distance
        case _:
            assert(False)
    min_x = min(x, min_x)
    max_x = max(x, max_x)
    min_y = min(y, min_y)
    max_y = max(y, max_y)

max_x = max_x - min_x
max_y = max_y - min_y

print(max_x, max_y)

class TileStatus(Enum):
    UNKNOWN = 1
    PATH = 2
    OUTSIDE = 3
    INSIDE = 4

tiles: list[list[TileStatus]] = [[TileStatus.UNKNOWN for _ in range(max_x+1)] for _ in range(max_y+1)]
print(len(tiles))
print(len(tiles[0]))

x=0
y=0
for instr in instructions:
    match instr.direction:
        case "R":
            x = x + instr.distance
        case "L":
            x = x - instr.distance
        case "D":
            y = y + instr.distance
        case "U":
            y = y - instr.distance
        case _:
            assert(False)
            