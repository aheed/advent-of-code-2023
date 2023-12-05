from dataclasses import dataclass
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

@dataclass
class Part:
    y: int
    x_first: int
    x_last: int

@dataclass(frozen=True)
class Point:
    x: int
    y: int

part_candidates: list[Part] = []

for y in range(len(lines)):
    part_found = False
    line = lines[y]
    x_first = 0
    for x in range(len(line)):
        char = line[x]        
        if part_found:
            if not char.isnumeric():
                part_candidates.append(Part(y=y, x_first=x_first, x_last=x-1))
                part_found = False
            elif x == (len(line) - 1):
                part_candidates.append(Part(y=y, x_first=x_first, x_last=x))
                part_found = False
        elif not part_found and char.isnumeric():
            x_first = x
            part_found = True

def is_in_bounds(cell: Point, max_x: int, max_y: int) -> bool:
    return cell.x >= 0 and cell.x <= max_x and cell.y >=0 and cell.y <= max_y

def get_neighbor_points(cell: Point, max_x: int, max_y: int) -> list[Point]:
    candidates = [
        Point(y=cell.y+1, x=cell.x+0),
        Point(y=cell.y+1, x=cell.x+1),
        Point(y=cell.y+0, x=cell.x+1),
        Point(y=cell.y-1, x=cell.x+1),
        Point(y=cell.y-1, x=cell.x+0),
        Point(y=cell.y-1, x=cell.x-1),
        Point(y=cell.y+0, x=cell.x-1),
        Point(y=cell.y+1, x=cell.x-1),
    ]
    return [cell for cell in candidates if is_in_bounds(cell=cell, max_x=max_x, max_y=max_y)]

def is_part_symbol(char: str) -> bool:
    return char != "." and not char.isnumeric()

max_x = len(lines[0]) - 1
max_y = len(lines) - 1

def is_adjacent_to_symbol(point: Point) -> bool:
    return any((is_part_symbol((lines[n.y])[n.x]) for n in get_neighbor_points(cell=point, max_x=max_x, max_y=max_y)))

def are_neighbors(p1: Point, p2: Point) -> bool:
    return any((candidate == p2 for candidate in get_neighbor_points(cell=p1, max_x=max_x, max_y=max_y)))

def is_valid_part(part: Part) -> bool:
    return any((is_adjacent_to_symbol(Point(x=x, y=part.y)) for x in range(part.x_first, part.x_last+1)))

parts = [p for p in part_candidates if is_valid_part(p)]

def get_part_number(part: Part) -> int:
    return int((lines[part.y])[part.x_first:part.x_last+1])

def is_part_adjecent_to_point(part: Part, point: Point) -> bool:
    if part.y - point.y > 1 or part.y - point.y < -1: # not necessary, just a quick check to speed things up
        return False
    return any((are_neighbors(point, neigh_point) for neigh_point in [Point(x=x, y=part.y) for x in range(part.x_first, part.x_last+1)]))

gear_ratios_sum = 0
for y in range(len(lines)):
    line = lines[y]
    for x in range(len(line)):
        char = line[x]        
        if char == "*":
            gear_point = Point(x=x, y=y)
            adjacent_parts = [part for part in parts if is_part_adjecent_to_point(part=part, point=gear_point)]
            if len(adjacent_parts) == 2:
                gear_ratio = get_part_number(adjacent_parts[0]) * get_part_number(adjacent_parts[1])
                print("gear at ", x, y, gear_ratio)
                gear_ratios_sum = gear_ratios_sum + gear_ratio
print(gear_ratios_sum)

