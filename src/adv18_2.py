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

def get_instruction_day_1(line: str) -> Instruction:
    parts = line.split(" ")
    return Instruction(direction=parts[0], distance=int(parts[1]), dbg=0)

instructions = [get_instruction(line) for line in lines]
#instructions = [get_instruction_day_1(line) for line in lines]
#print(instructions)


x_coord=0
y_coord=0
#min_x = x
#min_y = y
#max_x = x
#max_y = y
x_coords: list[int] = [x_coord]
y_coords: list[int] = [y_coord]
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

x_coords = list(set(x_coords)) #remove duplicates
y_coords = list(set(y_coords)) #remove duplicates
x_coords.sort()
y_coords.sort()

#print(x_coords, y_coords)
tiles: list[list[TileStatus]] = [[TileStatus.UNKNOWN for _ in range(1, len(x_coords))] for _ in range(1, len(y_coords))]


x_start_index = x_coords.index(0)
y_start_index = y_coords.index(0)
x_index = x_start_index
y_index = y_start_index
last_direction = instructions[-1].direction
extras = 0
orientation = 0
for instr in instructions:
    match instr.direction:
        case "R":
            match last_direction:
                case "U":
                    if x_index > 0:
                        if tiles[y_index][x_index-1] == TileStatus.UNKNOWN:
                            tiles[y_index][x_index-1] = TileStatus.OUTSIDE
                    if y_index > 0:
                        if tiles[y_index-1][x_index] == TileStatus.UNKNOWN:
                            tiles[y_index-1][x_index] = TileStatus.OUTSIDE
                    orientation = orientation + 1
                case "D":
                    extras = extras - 1
                    orientation = orientation - 1
                case _:
                    assert(False)
            target_x_coord = x_coords[x_index] + instr.distance
            extras = extras + instr.distance
            while x_coords[x_index] != target_x_coord:
                tiles[y_index][x_index] = TileStatus.INSIDE                
                if y_index > 0:
                    if tiles[y_index-1][x_index] == TileStatus.UNKNOWN:
                        tiles[y_index-1][x_index] = TileStatus.OUTSIDE
                x_index = x_index + 1
        case "L":
            match last_direction:
                case "D":
                    if x_index < (len(tiles[0])-1) and y_index < len(tiles):
                        if tiles[y_index][x_index+1] == TileStatus.UNKNOWN:
                            tiles[y_index][x_index+1] = TileStatus.OUTSIDE
                    if y_index < (len(tiles)-1) and x_index < len(tiles[0]):
                        if tiles[y_index+1][x_index] == TileStatus.UNKNOWN:
                            tiles[y_index+1][x_index] = TileStatus.OUTSIDE
                    orientation = orientation + 1
                case "U":
                    orientation = orientation - 1
                case _:
                    assert(False)
            target_x_coord = x_coords[x_index] - instr.distance
            while x_coords[x_index] != target_x_coord:
                if y_index > 0 and x_index > 0:
                    tiles[y_index-1][x_index-1] = TileStatus.INSIDE
                if y_index < (len(tiles)) and x_index > 0:
                    if tiles[y_index][x_index-1] == TileStatus.UNKNOWN:
                        tiles[y_index][x_index-1] = TileStatus.OUTSIDE
                x_index = x_index - 1
        case "D":
            match last_direction:
                case "L":
                    orientation = orientation - 1
                case "R":
                    if y_index > 0 and x_index < len(tiles[0]):
                        if tiles[y_index-1][x_index] == TileStatus.UNKNOWN:
                            tiles[y_index-1][x_index] = TileStatus.OUTSIDE
                    if x_index < (len(tiles[0])-1):
                        if tiles[y_index][x_index+1] == TileStatus.UNKNOWN:
                            tiles[y_index][x_index+1] = TileStatus.OUTSIDE
                    extras = extras + 1
                    orientation = orientation + 1
                case _:
                    assert(False)
            target_y_coord = y_coords[y_index] + instr.distance
            extras = extras + instr.distance
            while y_coords[y_index] != target_y_coord:
                if x_index > 0:
                    tiles[y_index][x_index-1] = TileStatus.INSIDE
                if x_index < len(tiles[0]):
                    if tiles[y_index][x_index] == TileStatus.UNKNOWN:
                        tiles[y_index][x_index] = TileStatus.OUTSIDE
                y_index = y_index + 1
        case "U":
            match last_direction:
                case "L":
                    if x_index > 0 and y_index < (len(tiles)-1):
                        if tiles[y_index][x_index-1] == TileStatus.UNKNOWN:
                            tiles[y_index][x_index-1] = TileStatus.OUTSIDE
                    if y_index < (len(tiles)-1):
                        if tiles[y_index+1][x_index] == TileStatus.UNKNOWN:
                            tiles[y_index+1][x_index] = TileStatus.OUTSIDE
                    orientation = orientation + 1
                case "R":
                    orientation = orientation - 1
                case _:
                    assert(False)
            target_y_coord = y_coords[y_index] - instr.distance
            while y_coords[y_index] != target_y_coord:
                if y_index > 0:
                    tiles[y_index-1][x_index] = TileStatus.INSIDE
                if x_index > 0 and y_index > 0:
                    if tiles[y_index-1][x_index-1] == TileStatus.UNKNOWN:
                        tiles[y_index-1][x_index-1] = TileStatus.OUTSIDE
                y_index = y_index - 1
        case _:
            assert(False)
    last_direction = instr.direction

assert(x_coord==0)
assert(y_coord==0)

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

#print_tiles()
#print("------")

dirty = True
while dirty:
    dirty = False
    for x in range(len(tiles[0])):
        for y in range(len(tiles)):
            if tiles[y][x] == TileStatus.UNKNOWN:
                dirty = True
                if x > 0:
                    neighbor_status = tiles[y][x-1]
                    if neighbor_status == TileStatus.INSIDE or neighbor_status == TileStatus.OUTSIDE:
                        tiles[y][x] = neighbor_status
                if y > 0:
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

#print_tiles()

def get_tile_size(x_index:int, y_index:int) -> int:
    width  = x_coords[x_index + 1] - x_coords[x_index]
    height = y_coords[y_index + 1] - y_coords[y_index]
    return width * height

sum_inside_tiles = sum([sum([get_tile_size(x_index=x, y_index=y) if tiles[y][x] == TileStatus.INSIDE else 0 for x in range(len(x_coords)-1)]) for y in range(len(y_coords)-1)])
assert(orientation == 4) # assume clockwise
#print(sum_inside_tiles)
#print(extras)
print(sum_inside_tiles + extras)

