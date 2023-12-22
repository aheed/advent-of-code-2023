from enum import Enum
from dataclasses import dataclass
import utils

@dataclass(frozen=True)
class Instruction:
    direction: str
    distance: int
    dbg: int

class TileStatus(Enum):
    UNKNOWN = 1
    OUTSIDE = 3
    INSIDE = 4

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

def get_direction(n: int) -> str:
    match n:
        case 0:
            return "R"
        case 1:
            return "D"
        case 2:
            return "L"
        case 3:
            return "U"
        case _:
            assert(False)

def get_instruction(line: str) -> Instruction:
    parts = line.split(" ")
    return Instruction(direction=get_direction(int(parts[2][-2:-1])), dbg=int(parts[1]), distance=int(parts[2][2:-2], 16))

instructions = [get_instruction(line) for line in lines]
#print(instructions)


x_coord=0
y_coord=0
#min_x = x
#min_y = y
#max_x = x
#max_y = y
x_coords: list[int] = [0]
y_coords: list[int] = [0]
for instr in instructions:
    match instr.direction:
        case "R":
            x_coord = x_coord + instr.distance
        case "L":
            x_coord = x_coord - instr.distance
        case "D":
            y_coord = y_coord + instr.distance
        case "U":
            y_coord = y_coord - instr.distance
        case _:
            assert(False)
    x_coords.append(x_coord)
    y_coords.append(y_coord)
    #min_x = min(x, min_x)
    #max_x = max(x, max_x)
    #min_y = min(y, min_y)
    #max_y = max(y, max_y)

#max_x = max_x - min_x
#max_y = max_y - min_y
x_coords = list(set(x_coords)) #remove duplicates
y_coords = list(set(y_coords)) #remove duplicates
x_coords.sort()
y_coords.sort()

print(x_coords, y_coords)
tiles: list[list[TileStatus]] = [[TileStatus.UNKNOWN for _ in range(len(x_coords))] for _ in range(len(x_coords))]


#################


#x_coord=0
#y_coord=0
x_index = 0
y_index = 0
last_direction = "U"
for instr in instructions:
    #x_index = x_coords.index(x)
    #y_index = y_coords.index(y)
    tiles[y_index][x_index] = TileStatus.INSIDE
    match instr.direction:
        case "R":
            match last_direction:
                case "U":
                    if tiles[y_index][x_index-1] == TileStatus.UNKNOWN:
                        tiles[y_index][x_index-1] = TileStatus.OUTSIDE
                    if tiles[y_index-1][x_index] == TileStatus.UNKNOWN:
                        tiles[y_index-1][x_index] = TileStatus.OUTSIDE
                case "D":
                    pass
                case _:
                    assert(False)
            target_x_coord = x_coords[x_index] + instr.distance
            while x_coords[x_index] != target_x_coord:
                tiles[y_index][x_index] = TileStatus.INSIDE
                if tiles[y_index-1][x_index] == TileStatus.UNKNOWN:
                    tiles[y_index-1][x_index] = TileStatus.OUTSIDE
                x_index = x_index + 1
        case "L":
            match last_direction:
                case "D":
                    if x_index < (len(tiles[0])-1):
                        if tiles[y_index][x_index+1] == TileStatus.UNKNOWN:
                            tiles[y_index][x_index+1] = TileStatus.OUTSIDE
                    if y_index < (len(tiles)-1):
                        if tiles[y_index+1][x_index] == TileStatus.UNKNOWN:
                            tiles[y_index+1][x_index] = TileStatus.OUTSIDE
                case "U":
                    pass
                case _:
                    assert(False)
            target_x_coord = x_coords[x_index] - instr.distance
            while x_coords[x_index] != target_x_coord:
                tiles[y_index][x_index] = TileStatus.INSIDE
                if tiles[y_index+1][x_index] == TileStatus.UNKNOWN:
                    tiles[y_index+1][x_index] = TileStatus.OUTSIDE
                x_index = x_index - 1
        case "D":
            match last_direction:
                case "L":
                    pass
                case "R":
                    if tiles[y_index-1][x_index] == TileStatus.UNKNOWN:
                        tiles[y_index-1][x_index] = TileStatus.OUTSIDE
                    if x_index < (len(tiles[0])-1):
                        if tiles[y_index][x_index+1] == TileStatus.UNKNOWN:
                            tiles[y_index][x_index+1] = TileStatus.OUTSIDE
                case _:
                    assert(False)
            target_y_coord = y_coords[y_index] + instr.distance
            while y_coords[y_index] != target_y_coord:
                tiles[y_index][x_index] = TileStatus.INSIDE
                if x_index < (len(tiles[0])-1):
                    if tiles[y_index][x_index+1] == TileStatus.UNKNOWN:
                        tiles[y_index][x_index+1] = TileStatus.OUTSIDE
                y_index = y_index + 1
        case "U":
            match last_direction:
                case "L":
                    if tiles[y_index][x_index-1] == TileStatus.UNKNOWN:
                        tiles[y_index][x_index-1] = TileStatus.OUTSIDE
                    if y_index < (len(tiles)-1):
                        if tiles[y_index+1][x_index] == TileStatus.UNKNOWN:
                            tiles[y_index+1][x_index] = TileStatus.OUTSIDE
                case "R":
                    pass
                case _:
                    assert(False)
            target_y_coord = y_coords[y_index] - instr.distance
            while y_coords[y_index] != target_y_coord:
                tiles[y_index][x_index] = TileStatus.INSIDE
                if tiles[y_index][x_index-1] == TileStatus.UNKNOWN:
                    tiles[y_index][x_index-1] = TileStatus.OUTSIDE
                y_index = y_index - 1
        case _:
            assert(False)
    last_direction = instr.direction

assert(x_coord==0)
assert(y_coord==0)
assert(x_index==0)
assert(y_index==0)

#################
def status_to_char(status: TileStatus) -> str:
    match status:
        case TileStatus.UNKNOWN:
            return "?"
        case TileStatus.INSIDE:
            return "I"
        case TileStatus.OUTSIDE:
            return "O"

def print_tiles():
    global tiles
    for row in tiles:
        print("".join([status_to_char(s) for s in row]))

print_tiles()
print("------")

dirty = True
while dirty:
    dirty = False
    for x in range(len(tiles[0])):
        for y in range(len(tiles)):
            if tiles[y][x] == TileStatus.UNKNOWN:
                dirty = True
                neighbor_status = tiles[y][x-1]
                if neighbor_status == TileStatus.INSIDE or neighbor_status == TileStatus.OUTSIDE:
                    tiles[y][x] = neighbor_status
                    neighbor_status = tiles[y-1][x]
                    if neighbor_status == TileStatus.INSIDE or neighbor_status == TileStatus.OUTSIDE:
                        tiles[y][x] = neighbor_status
                if x < len(tiles[0])-1:
                    neighbor_status = tiles[y][x+1]
                    if neighbor_status == TileStatus.INSIDE or neighbor_status == TileStatus.OUTSIDE:
                        tiles[y][x] = neighbor_status
                if y < len(tiles)-1:
                    neighbor_status = tiles[y+1][x]
                    if neighbor_status == TileStatus.INSIDE or neighbor_status == TileStatus.OUTSIDE:
                        tiles[y][x] = neighbor_status

print_tiles()

def get_tile_size(x_index:int, y_index:int) -> int:
    width  = x_coords[x_index] - (x_coords[x_index-1] if x_index > 0 else 0)
    height = y_coords[y_index] - (y_coords[y_index-1] if y_index > 0 else 0)
    return width * height

sum_inside_tiles = sum([sum([get_tile_size(x_index=x, y_index=y) if tiles[y][x] == TileStatus.INSIDE else 0 for x in range(len(x_coords))]) for y in range(len(y_coords))])
print(sum_inside_tiles)

#################

"""
def instruction_to_command(instructions: list[Instruction], index: int) -> int:
    
    match instructions[index].direction:
        case "R":
            match instructions[index-1].direction:
                case "D":
                    multiplier = -1
                case "U":
                    multiplier = 1
                case _:
                    assert(False)        
        case "L":
            match instructions[index-1].direction:
                case "D":
                    multiplier = 1
                case "U":
                    multiplier = -1
                case _:
                    assert(False)
        case "D":
            match instructions[index-1].direction:
                case "R":
                    multiplier = 1
                case "L":
                    multiplier = -1
                case _:
                    assert(False)
        case "U":
            match instructions[index-1].direction:
                case "R":
                    multiplier = -1
                case "L":
                    multiplier = 1
                case _:
                    assert(False)
        case _:
            assert(False)
    return instructions[index].distance * multiplier

commands = [instruction_to_command(instructions=instructions, index=index) for index in range(len(instructions))]
print(commands)
"""

#############
"""
Rewrite reading of values (use the hex code)
Verify it's a loop
Convert to sequence of LR instructions instead of orientation

while not done:
    identify RR:
      reduce 0 and 2 by min(0 ,2)
      add 1 * min(0, 2) to total
    identify instructions with 0 distance
      -1 = -1 + 1
      remove 0 and 1

while True:
    identify LRR
      if not found
        break
      reduce 0 and 2 by min(0 ,2)
      add 1 * min(0, 2) to total

cases:
  0 < 2
  2 < 0
  -1 is L
  -1 is R
  3 is L
  3 is R

Assume LRR:
0 < 2
  -1 or 3 does not matter

2 > 0
  3 is L
    still works
  3 is R
    ?

----------
with positive values for right turns:

identify instructions with 0 distance
      -1 = -1 - 1
      0 = - 2
      remove 1 and 2
"""