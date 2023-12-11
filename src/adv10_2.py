from enum import Enum
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

class TileStatus(Enum):
    UNKNOWN = 1
    PATH = 2
    OUTSIDE = 3
    INSIDE = 4

tiles: list[list[TileStatus]] = [[TileStatus.UNKNOWN for _ in line] for line in lines]

y_s = 0
while True:
    if "S" in lines[y_s]:
        x_s = lines[y_s].index("S")
        break
    y_s = y_s + 1

print(x_s,y_s)
print(lines[y_s][x_s])

tiles[y_s][x_s] = TileStatus.PATH
found = False
x = x_s
y = y_s
direction = "e"
orientation = 0
c = lines[y_s][x_s]

east = lines[y_s][x_s+1]
if east == "-":
    x = x_s+1
    y = y_s
    found = True

if east == "J":
    x = x_s+1
    y = y_s-1
    direction = "n"
    orientation = orientation - 90
    found = True

if east == "7":
    x = x_s+1
    y = y_s+1
    direction = "s"
    orientation = orientation + 90
    found = True

# todo: handle the case you can't start going east
assert(found)

cnt = 2
while not (x == x_s and y == y_s):
    c = lines[y][x]
    tiles[y][x] = TileStatus.PATH

    print(cnt, x, y, c, direction, orientation)

    if direction == "e":
        if c == "-":
            if y > 0:
                if tiles[y-1][x] == TileStatus.UNKNOWN:
                    tiles[y-1][x] = TileStatus.OUTSIDE
            if y < (len(tiles)-1):
                if tiles[y+1][x] == TileStatus.UNKNOWN:
                    tiles[y+1][x] = TileStatus.INSIDE
            x = x + 1            
        elif c == "J":
            if x < (len(tiles[0])-1):
                if tiles[y][x+1] == TileStatus.UNKNOWN:
                    tiles[y][x+1] = TileStatus.INSIDE
            if y < (len(tiles)-1):
                if tiles[y+1][x] == TileStatus.UNKNOWN:
                    tiles[y+1][x] = TileStatus.INSIDE
            y = y - 1
            direction = "n"
            orientation = orientation - 90
        elif c == "7":
            if y > 0:
                if tiles[y-1][x] == TileStatus.UNKNOWN:
                    tiles[y-1][x] = TileStatus.OUTSIDE
            if x < (len(tiles[0])-1):
                if tiles[y][x+1] == TileStatus.UNKNOWN:
                    tiles[y][x+1] = TileStatus.OUTSIDE
            y = y + 1
            direction = "s"
            orientation = orientation + 90
    elif direction == "w":
        if c == "-":
            if y > 0:
                if tiles[y-1][x] == TileStatus.UNKNOWN:
                    tiles[y-1][x] = TileStatus.INSIDE
            if y < (len(tiles)-1):
                if tiles[y+1][x] == TileStatus.UNKNOWN:
                    tiles[y+1][x] = TileStatus.OUTSIDE
            x = x - 1
        elif c == "L":
            if x > 0:
                if tiles[y][x-1] == TileStatus.UNKNOWN:
                    tiles[y][x-1] = TileStatus.OUTSIDE
            if y < (len(tiles)-1):
                if tiles[y+1][x] == TileStatus.UNKNOWN:
                    tiles[y+1][x] = TileStatus.OUTSIDE
            y = y - 1
            direction = "n"
            orientation = orientation + 90
        elif c == "F":
            if y > 0:
                if tiles[y-1][x] == TileStatus.UNKNOWN:
                    tiles[y-1][x] = TileStatus.INSIDE
            if x > 0:
                if tiles[y][x-1] == TileStatus.UNKNOWN:
                    tiles[y][x-1] = TileStatus.INSIDE
            y = y + 1
            direction = "s"
            orientation = orientation - 90
    elif direction == "n":
        if c == "|":
            if x < (len(tiles[0])-1):
                if tiles[y][x+1] == TileStatus.UNKNOWN:
                    tiles[y][x+1] = TileStatus.INSIDE
            if x > 0:
                if tiles[y][x-1] == TileStatus.UNKNOWN:
                    tiles[y][x-1] = TileStatus.OUTSIDE
            y = y - 1
        elif c == "7":
            if x < (len(tiles[0])-1):
                if tiles[y][x+1] == TileStatus.UNKNOWN:
                    tiles[y][x+1] = TileStatus.INSIDE
            if y > 0:
                if tiles[y-1][x] == TileStatus.UNKNOWN:
                    tiles[y-1][x] = TileStatus.INSIDE
            x = x - 1
            direction = "w"
            orientation = orientation - 90
        elif c == "F":
            if x > 0:
                if tiles[y][x-1] == TileStatus.UNKNOWN:
                    tiles[y][x-1] = TileStatus.OUTSIDE
            if y > 0:
                if tiles[y-1][x] == TileStatus.UNKNOWN:
                    tiles[y-1][x] = TileStatus.OUTSIDE
            x = x + 1
            direction = "e"
            orientation = orientation + 90
    elif direction == "s":
        if c == "|":
            if x < (len(tiles[0])-1):
                if tiles[y][x+1] == TileStatus.UNKNOWN:
                    tiles[y][x+1] = TileStatus.OUTSIDE
            if x > 0:
                if tiles[y][x-1] == TileStatus.UNKNOWN:
                    tiles[y][x-1] = TileStatus.INSIDE
            y = y + 1
        elif c == "J":
            if x < (len(tiles[0])-1):
                if tiles[y][x+1] == TileStatus.UNKNOWN:
                    tiles[y][x+1] = TileStatus.OUTSIDE
            if y < (len(tiles)-1):
                if tiles[y+1][x] == TileStatus.UNKNOWN:
                    tiles[y+1][x] = TileStatus.OUTSIDE
            x = x - 1
            direction = "w"
            orientation = orientation + 90
        elif c == "L":
            if x > 0:
                if tiles[y][x-1] == TileStatus.UNKNOWN:
                    tiles[y][x-1] = TileStatus.INSIDE
            if y < (len(tiles)-1):
                if tiles[y+1][x] == TileStatus.UNKNOWN:
                    tiles[y+1][x] = TileStatus.INSIDE
            x = x + 1
            direction = "e"
            orientation = orientation - 90
   
    cnt = cnt + 1

print("---")
print(cnt, x, y, c, direction, orientation)
print(cnt)
print(cnt // 2)

# 2-dim grid of tiles
# tile status can be unknown, path, inside, outside
# iterate path: all neighbors on the right side are inside, neighbors on the left are outside
# iterate all tiles: if there is any unknown tile, check if any of it's neighbors is outside or inside
#  repeat until no more unknown tiles



print(tiles)
for tl in tiles:
    print("".join([f"{tile.value}" for tile in tl]))

dirty = True
while dirty:
    print("floodfilling")
    unknown_cnt = 0
    for x in range(len(tiles[0])):
        for y in range(len(tiles)):
            if tiles[y][x] == TileStatus.UNKNOWN:
                unknown_cnt = unknown_cnt + 1
                print(x,y)
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
    dirty = unknown_cnt > 0
    #dirty = False #temp

print(tiles)
for tl in tiles:
    print("".join([f"{tile.value}" for tile in tl]))

print(sum([sum([1 if tile == TileStatus.INSIDE else 0 for tile in tl]) for tl in tiles]))