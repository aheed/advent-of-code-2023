from dataclasses import dataclass
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

@dataclass
class Galaxy:
    x: int
    y: int

nof_lines = len(lines)
nof_columns = len(lines[0])
max_y = nof_lines-1
max_x = nof_columns-1

galaxies: list[Galaxy] = []

for x in range(nof_columns):
    for y in range(nof_lines):
        c = lines[y][x]
        if c == "#":
            galaxies.append(Galaxy(x=x, y=y))
#print(galaxies, len(galaxies))

def calc_extra_rows(line: str) -> int:
    return 0 if any((c=="#" for c in line)) else 1

def calc_extra_columns(x: int) -> int:
    return 0 if any((lines[y][x] =="#" for y in range(nof_lines))) else 1

row_thickness = [calc_extra_rows(line=line) + 1 for line in lines]
column_thickness = [calc_extra_columns(x=x) +1 for x in range(nof_columns)]
#print(row_thickness)
#print(column_thickness)

pairs: list[list[Galaxy]] = []
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        pairs.append([galaxies[i], galaxies[j]])

def calc_shortest_path(pair: list[Galaxy]) -> int:
    min_x = min(pair[0].x, pair[1].x)
    max_x = max(pair[0].x, pair[1].x)
    x_distance = 0
    for x in range(min_x, max_x):
        x_distance = x_distance + column_thickness[x]

    min_y = min(pair[0].y, pair[1].y)
    max_y = max(pair[0].y, pair[1].y)
    y_distance = 0
    for y in range(min_y, max_y):
        y_distance = y_distance + row_thickness[y]

    return x_distance + y_distance

shortest_paths = [calc_shortest_path(pair=pair) for pair in pairs]
#print(shortest_paths)
print(sum(shortest_paths))