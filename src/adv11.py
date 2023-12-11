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
print(galaxies, len(galaxies))



pairs: list[list[Galaxy]] = []
#for i in range((len(galaxies)+1)//2):
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        print(i,j)
        pairs.append([galaxies[i], galaxies[j]])

print(pairs, len(pairs))

shortest_paths = [abs(pair[0].x - pair[1].x) + abs(pair[0].y - pair[1].y) for pair in pairs]
print(shortest_paths)
print(sum(shortest_paths))