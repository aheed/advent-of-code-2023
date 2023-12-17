from dataclasses import dataclass
import utils


@dataclass
class Position:
    x: int
    y: int

@dataclass
class Node:
    position: Position
    visited: bool
    best: int
    heat_loss: int

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

grid = [[int(c) for c in line] for line in lines]
#print(grid)

bad_heat_loss = 1000000000

nodes = [Node(position=Position(x=x, y=y), visited=False, best=bad_heat_loss, heat_loss=grid[y][x]) for x in range(len(grid[0])) for y in range(len(grid))]

first_pos = Position(x=0, y=0)
first_index = next((i for i in range(len(nodes)) if nodes[i].position == first_pos))
nodes[first_index].best = 0
current_pos = first_pos
while True:
    current_index = next((i for i in range(len(nodes)) if nodes[i].position == current_pos))
    neigh_positions = [p for p in [
            Position(x=current_pos.x+1, y=current_pos.y),
            Position(x=current_pos.x-1, y=current_pos.y),
            Position(x=current_pos.x, y=current_pos.y-1),
            Position(x=current_pos.x, y=current_pos.y+1)]
        if (p.x >= 0 and p.x < len(grid[0]) and p.y >=0 and p.y < len(grid))]
    for neigh_pos in neigh_positions:
        neigh_index = next((i for i in range(len(nodes)) if nodes[i].position == neigh_pos))
        if not nodes[neigh_index].visited:
            nodes[neigh_index].best = min(nodes[neigh_index].best, nodes[neigh_index].heat_loss + nodes[current_index].best)
    nodes[current_index].visited = True

    lowest_unvisited_best = bad_heat_loss
    lowest_unvisited_index = -1
    for i in range(len(nodes)):
        if (not nodes[i].visited) and nodes[i].best < lowest_unvisited_best:
            lowest_unvisited_index = i
    if lowest_unvisited_index == -1:
        break
    current_pos = nodes[lowest_unvisited_index].position

print(nodes)
print(len(nodes))

end_node = next((n for n in nodes if n.position == Position(x=len(grid[0])-1, y=len(grid)-1)))
print(end_node)