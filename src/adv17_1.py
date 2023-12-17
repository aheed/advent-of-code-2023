from dataclasses import dataclass
import utils

@dataclass
class SearchInput:
    direction: str
    x: int
    y:int
    heat_loss: int
    moves_in_same_direction: int

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

grid = [[int(c) for c in line] for line in lines]
#print(grid)

visited = [[False for _ in row] for row in grid]

cache: dict[str, int] = {}

bad_heat_loss = 1000000000

def traverse_grid(search_input: SearchInput) -> int:

    global visited
    global cache

    if search_input.moves_in_same_direction > 3:
        return bad_heat_loss

    if search_input.x < 0 or search_input.x > len(grid[0])-1 or search_input.y < 0 or search_input.y > len(grid)-1:
        return bad_heat_loss

    key = f"{search_input.x},{search_input.y}:{search_input.direction}z{search_input.moves_in_same_direction}"
    if key in cache:
        return cache[key]
    
    if visited[search_input.y][search_input.x]:
        return bad_heat_loss
    visited[search_input.y][search_input.x] = True    

    min_heat_loss = search_input.heat_loss + grid[search_input.y][search_input.x]
    if not (search_input.x == len(grid[0])-1 and search_input.y == len(grid)-1):
        new_searches: list[SearchInput] = []
        match search_input.direction:
            case "e":
                new_searches = [
                    SearchInput(direction="e", x=search_input.x+1, y=search_input.y, heat_loss=min_heat_loss, moves_in_same_direction=search_input.moves_in_same_direction+1),
                    SearchInput(direction="n", x=search_input.x, y=search_input.y-1, heat_loss=min_heat_loss, moves_in_same_direction=1),
                    SearchInput(direction="s", x=search_input.x, y=search_input.y+1, heat_loss=min_heat_loss, moves_in_same_direction=1)
                ]
            case "w":
                new_searches = [
                    SearchInput(direction="w", x=search_input.x-1, y=search_input.y, heat_loss=min_heat_loss, moves_in_same_direction=search_input.moves_in_same_direction+1),
                    SearchInput(direction="n", x=search_input.x, y=search_input.y-1, heat_loss=min_heat_loss, moves_in_same_direction=1),
                    SearchInput(direction="s", x=search_input.x, y=search_input.y+1, heat_loss=min_heat_loss, moves_in_same_direction=1)
                ]
            case "n":
                new_searches = [
                    SearchInput(direction="n", x=search_input.x, y=search_input.y-1, heat_loss=min_heat_loss, moves_in_same_direction=search_input.moves_in_same_direction+1),
                    SearchInput(direction="e", x=search_input.x+1, y=search_input.y, heat_loss=min_heat_loss, moves_in_same_direction=1),
                    SearchInput(direction="w", x=search_input.x-1, y=search_input.y, heat_loss=min_heat_loss, moves_in_same_direction=1)
                ]
            case "s":
                new_searches = [
                    SearchInput(direction="s", x=search_input.x, y=search_input.y+1, heat_loss=min_heat_loss, moves_in_same_direction=search_input.moves_in_same_direction+1),
                    SearchInput(direction="e", x=search_input.x+1, y=search_input.y, heat_loss=min_heat_loss, moves_in_same_direction=1),
                    SearchInput(direction="w", x=search_input.x-1, y=search_input.y, heat_loss=min_heat_loss, moves_in_same_direction=1)
                ]

            case _:
                assert(False)
        search_results = [traverse_grid(search_input=s) for s in new_searches]
        min_heat_loss = min(min_heat_loss, min(search_results))

    visited[search_input.y][search_input.x] = False
    cache[key] = min_heat_loss
    return min_heat_loss

res = traverse_grid(search_input=SearchInput(direction="e", x=0, y=0, heat_loss=0, moves_in_same_direction=0))
print(res)

