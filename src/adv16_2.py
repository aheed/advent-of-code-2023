import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

grid = [[c for c in line] for line in lines]
#print(grid)

beam_cnts = [[0 for _ in row] for row in grid]
#print(beam_cnts)

cache: dict[str, int] = {}

def traverse_grid(direction: str, x: int, y:int):
    while not (x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid)):
        key = f"{x},{y}:{direction}"
        if key in cache:
            return
        cache[key] = 1

        beam_cnts[y][x] = beam_cnts[y][x] + 1
        c =  grid[y][x]
        match direction:
            case "e":
                match c:
                    case "." | "-":
                        x = x + 1
                    case "/":
                        direction = "n"
                        y = y - 1
                    case "\\":
                        direction = "s"
                        y = y + 1
                    case "|":
                        direction = "s"
                        y = y + 1
                        traverse_grid(direction="n", x=x, y=y-1)
                    case _:
                        assert(False)
            case "w":
                match c:
                    case "." | "-":
                        x = x - 1
                    case "/":
                        direction = "s"
                        y = y + 1
                    case "\\":
                        direction = "n"
                        y = y - 1
                    case "|":
                        direction = "s"
                        y = y + 1
                        traverse_grid(direction="n", x=x, y=y-1)
                    case _:
                        assert(False)
            case "n":
                match c:
                    case "." | "|":
                        y = y - 1
                    case "/":
                        direction = "e"
                        x = x + 1
                    case "\\":
                        direction = "w"
                        x = x - 1
                    case "-":
                        direction = "w"
                        x = x - 1
                        traverse_grid(direction="e", x=x+1, y=y)
                    case _:
                        assert(False)
            case "s":
                match c:
                    case "." | "|":
                        y = y + 1
                    case "/":
                        direction = "w"
                        x = x - 1
                    case "\\":
                        direction = "e"
                        x = x + 1
                    case "-":
                        direction = "w"
                        x = x - 1
                        traverse_grid(direction="e", x=x+1, y=y)
                    case _:
                        assert(False)
            case _:
                assert(False)

###

def calc_sum() -> int:
    return sum((sum((1 for cnt in row if cnt > 0 )) for row in beam_cnts))

def reset():
    global beam_cnts
    global cache
    beam_cnts = [[0 for _ in row] for row in grid]
    cache = {}

max_sum = 0
#for direction in ["e", "w"]:
for y in range(len(grid)):        
    reset()
    traverse_grid(direction="e", x=0, y=y)
    s = calc_sum()
    max_sum = max(max_sum, s)

for y in range(len(grid)):
    reset()
    traverse_grid(direction="w", x=len(grid[0])-1, y=y)
    s = calc_sum()
    max_sum = max(max_sum, s)

for x in range(len(grid[0])):
    reset()
    traverse_grid(direction="s", x=x, y=0)
    s = calc_sum()
    max_sum = max(max_sum, s)

for x in range(len(grid[0])):
    reset()
    traverse_grid(direction="n", x=x, y=len(grid)-1)
    s = calc_sum()
    max_sum = max(max_sum, s)

print(max_sum)

###
#traverse_grid(direction="e", x = 0, y=0)
#print(beam_cnts)
#s = sum((sum((1 for cnt in row if cnt > 0 )) for row in beam_cnts))
#print(s)