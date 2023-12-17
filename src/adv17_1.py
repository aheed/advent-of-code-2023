import sys
from dataclasses import dataclass
import utils

@dataclass
class SearchInput:
    direction: str
    x: int
    y:int
    #heat_loss: int
    moves_in_same_direction: int

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

grid = [[int(c) for c in line] for line in lines]
#print(grid)


cache: dict[str, int] = {}
visited: set[str] = set([])
visited0 = [[False for _ in row] for row in grid]

bad_heat_loss = 1000000000

def gen_key(search_input: SearchInput) -> str:
    return f"{search_input.x},{search_input.y}:{search_input.direction}z{search_input.moves_in_same_direction}" 

def traverse_grid(search_input: SearchInput) -> int:

    global visited
    global visited0
    global cache

    if search_input.moves_in_same_direction > 3:
        return bad_heat_loss

    if search_input.x < 0 or search_input.x > len(grid[0])-1 or search_input.y < 0 or search_input.y > len(grid)-1:
        return bad_heat_loss

    #key = f"{search_input.x},{search_input.y}:{search_input.direction}z{search_input.moves_in_same_direction}"
    key = gen_key(search_input=search_input)
    if key in cache:
        return cache[key]
        #pass #temp

    #if visited0[search_input.y][search_input.x]:
    #    return bad_heat_loss
    #visited0[search_input.y][search_input.x] = True

    if key == "10,4:sz2":
        print("zzz")

    if key in visited:
        return bad_heat_loss
    visited.add(key)

    min_heat_loss = grid[search_input.y][search_input.x] #fixme: should not count for start city block
    if not (search_input.x == len(grid[0])-1 and search_input.y == len(grid)-1):
        new_searches: list[SearchInput] = []
        match search_input.direction:
            case "e":
                new_searches = [
                    SearchInput(direction="e", x=search_input.x+1, y=search_input.y, moves_in_same_direction=search_input.moves_in_same_direction+1),
                    SearchInput(direction="n", x=search_input.x, y=search_input.y-1, moves_in_same_direction=1),
                    SearchInput(direction="s", x=search_input.x, y=search_input.y+1, moves_in_same_direction=1)
                ]
            case "w":
                new_searches = [
                    SearchInput(direction="w", x=search_input.x-1, y=search_input.y, moves_in_same_direction=search_input.moves_in_same_direction+1),
                    SearchInput(direction="n", x=search_input.x, y=search_input.y-1, moves_in_same_direction=1),
                    SearchInput(direction="s", x=search_input.x, y=search_input.y+1, moves_in_same_direction=1)
                ]
            case "n":
                new_searches = [
                    SearchInput(direction="n", x=search_input.x, y=search_input.y-1, moves_in_same_direction=search_input.moves_in_same_direction+1),
                    SearchInput(direction="e", x=search_input.x+1, y=search_input.y, moves_in_same_direction=1),
                    SearchInput(direction="w", x=search_input.x-1, y=search_input.y, moves_in_same_direction=1)
                ]
            case "s":
                new_searches = [
                    SearchInput(direction="s", x=search_input.x, y=search_input.y+1, moves_in_same_direction=search_input.moves_in_same_direction+1),
                    SearchInput(direction="e", x=search_input.x+1, y=search_input.y, moves_in_same_direction=1),
                    SearchInput(direction="w", x=search_input.x-1, y=search_input.y, moves_in_same_direction=1)
                ]

            case _:
                assert(False)
        search_results = [traverse_grid(search_input=s) for s in new_searches]
        min_heat_loss = min_heat_loss + min(search_results)
    else:
        print("got to the finish line", search_input.x, search_input.y)

    visited.remove(key)
    #visited0[search_input.y][search_input.x] = False
    cache[key] = min_heat_loss
    return min_heat_loss

sys.setrecursionlimit(25000)
res = traverse_grid(search_input=SearchInput(direction="e", x=0, y=0, moves_in_same_direction=0))
res = res - grid[0][0]
print(res)

print("--------")
print(cache["1,0:ez1"]) #123

print(cache["9,2:ez1"]) # 65
print(cache["10,2:ez2"]) # 61
print(cache["10,3:sz1"]) # 59
print(cache["10,4:sz2"]) # 55 ??? should not be 59!! 

# The problem: cache entries are is created with incorrect "cycled" results

print(cache["11,4:ez1"]) #50  This alternative is in visited, not in cache when "10,4:sz2" is evaluated.
print(cache["11,5:sz1"]) #47
print(cache["11,6:sz2"]) #42
print(cache["11,7:sz3"]) #36
print(cache["12,7:ez1"])
print(cache["12,8:sz1"])
print(cache["12,9:sz2"])
print(cache["12,10:sz3"])
print(cache["11,10:wz1"])
print(cache["11,11:sz1"])
print(cache["11,12:sz2"])
print(cache["12,12:ez1"])


# 771 is too high

