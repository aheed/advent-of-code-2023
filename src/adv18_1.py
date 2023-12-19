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
last_direction = "U"
for instr in instructions:
    tiles[y][x] = TileStatus.PATH
    match instr.direction:
        case "R":
            match last_direction:
                case "D":
                    if x > 0:
                        if tiles[y][x-1] == TileStatus.UNKNOWN:
                            tiles[y][x-1] = TileStatus.INSIDE
                    if y < (len(tiles)-1):
                        if tiles[y+1][x] == TileStatus.UNKNOWN:
                            tiles[y+1][x] = TileStatus.INSIDE
                case "U":
                    if x > 0:
                        if tiles[y][x-1] == TileStatus.UNKNOWN:
                            tiles[y][x-1] = TileStatus.OUTSIDE
                    if y > 0:
                        if tiles[y-1][x] == TileStatus.UNKNOWN:
                            tiles[y-1][x] = TileStatus.OUTSIDE
                case _:
                    assert(False)
            x = x + 1
            for _ in range(instr.distance-1):
                tiles[y][x] = TileStatus.PATH
                if y > 0:
                    if tiles[y-1][x] == TileStatus.UNKNOWN:
                        tiles[y-1][x] = TileStatus.OUTSIDE
                if y < (len(tiles)-1):
                    if tiles[y+1][x] == TileStatus.UNKNOWN:
                        tiles[y+1][x] = TileStatus.INSIDE
                x = x + 1
        case "L":
            match last_direction:
                case "D":
                    if x < (len(tiles[0])-1):
                        if tiles[y][x+1] == TileStatus.UNKNOWN:
                            tiles[y][x+1] = TileStatus.OUTSIDE
                    if y < (len(tiles)-1):
                        if tiles[y+1][x] == TileStatus.UNKNOWN:
                            tiles[y+1][x] = TileStatus.OUTSIDE
                case "U":
                    if x < (len(tiles[0])-1):
                        if tiles[y][x+1] == TileStatus.UNKNOWN:
                            tiles[y][x+1] = TileStatus.INSIDE
                    if y > 0:
                        if tiles[y-1][x] == TileStatus.UNKNOWN:
                            tiles[y-1][x] = TileStatus.INSIDE
                case _:
                    assert(False)
            x = x - 1
            for _ in range(instr.distance-1):
                tiles[y][x] = TileStatus.PATH                
                if y > 0:
                    if tiles[y-1][x] == TileStatus.UNKNOWN:
                        tiles[y-1][x] = TileStatus.INSIDE
                if y < (len(tiles)-1):
                    if tiles[y+1][x] == TileStatus.UNKNOWN:
                        tiles[y+1][x] = TileStatus.OUTSIDE
                x = x - 1
        case "D":
            match last_direction:
                case "L":
                    if y > 0:
                        if tiles[y-1][x] == TileStatus.UNKNOWN:
                            tiles[y-1][x] = TileStatus.INSIDE
                    if x > 0:
                        if tiles[y][x-1] == TileStatus.UNKNOWN:
                            tiles[y][x-1] = TileStatus.INSIDE
                case "R":
                    if y > 0:
                        if tiles[y-1][x] == TileStatus.UNKNOWN:
                            tiles[y-1][x] = TileStatus.OUTSIDE
                    if x < (len(tiles[0])-1):
                        if tiles[y][x+1] == TileStatus.UNKNOWN:
                            tiles[y][x+1] = TileStatus.OUTSIDE
                case _:
                    assert(False)
            y = y + 1
            for _ in range(instr.distance-1):
                tiles[y][x] = TileStatus.PATH                
                if x < (len(tiles[0])-1):
                    if tiles[y][x+1] == TileStatus.UNKNOWN:
                        tiles[y][x+1] = TileStatus.OUTSIDE
                if x > 0:
                    if tiles[y][x-1] == TileStatus.UNKNOWN:
                        tiles[y][x-1] = TileStatus.INSIDE
                y = y + 1
        case "U":
            match last_direction:
                case "L":
                    if x > 0:
                        if tiles[y][x-1] == TileStatus.UNKNOWN:
                            tiles[y][x-1] = TileStatus.OUTSIDE
                    if y < (len(tiles)-1):
                        if tiles[y+1][x] == TileStatus.UNKNOWN:
                            tiles[y+1][x] = TileStatus.OUTSIDE
                case "R":
                    if x < (len(tiles[0])-1):
                        if tiles[y][x+1] == TileStatus.UNKNOWN:
                            tiles[y][x+1] = TileStatus.INSIDE
                    if y < (len(tiles)-1):
                        if tiles[y+1][x] == TileStatus.UNKNOWN:
                            tiles[y+1][x] = TileStatus.INSIDE
                case _:
                    assert(False)
            y = y - 1
            for _ in range(instr.distance-1):
                tiles[y][x] = TileStatus.PATH                
                if x < (len(tiles[0])-1):
                    if tiles[y][x+1] == TileStatus.UNKNOWN:
                        tiles[y][x+1] = TileStatus.INSIDE
                if x > 0:
                    if tiles[y][x-1] == TileStatus.UNKNOWN:
                        tiles[y][x-1] = TileStatus.OUTSIDE
                y = y - 1
        case _:
            assert(False)
    last_direction = instr.direction

assert(x==0)
assert(y==0)

def status_to_char(status: TileStatus) -> str:
    match status:
        case TileStatus.UNKNOWN:
            return "?"
        case TileStatus.PATH:
            return "#"
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

print_tiles()

nof_path_tiles = sum([sum([1 if tile == TileStatus.PATH else 0 for tile in tl]) for tl in tiles])
print(nof_path_tiles)
nof_inside_tiles = sum([sum([1 if tile == TileStatus.INSIDE else 0 for tile in tl]) for tl in tiles])
print(nof_inside_tiles)
nof_outside_tiles = sum([sum([1 if tile == TileStatus.OUTSIDE else 0 for tile in tl]) for tl in tiles])
print(nof_outside_tiles)
print(nof_path_tiles + nof_inside_tiles)