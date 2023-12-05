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
                print("zzz", y, x_first, x)
        elif not part_found and char.isnumeric():
            x_first = x
            part_found = True

#print(part_candidates)


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

def is_valid_part(part: Part) -> bool:
    return any((is_adjacent_to_symbol(Point(x=x, y=part.y)) for x in range(part.x_first, part.x_last+1)))

parts = [p for p in part_candidates if is_valid_part(p)]
#print(parts)

def get_part_number(part: Part) -> int:
    return int((lines[part.y])[part.x_first:part.x_last+1])

print(sum([get_part_number(p) for p in parts]))
#print([(lines[part.y])[part.x_first:part.x_last+1] for part in parts])
