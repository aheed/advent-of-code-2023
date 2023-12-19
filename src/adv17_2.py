from dataclasses import dataclass
import utils

@dataclass(frozen=True)
class NodeId:
    x: int
    y: int
    direction: str
    steps_forward: int

@dataclass
class Node:
    #id: NodeId
    visited: bool
    best: int
    heat_loss: int

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

grid = [[int(c) for c in line] for line in lines]
grid[0][0] = 0

bad_heat_loss = 1000000000

def get_neighbors(id: NodeId) -> list[NodeId]:
    match id.direction:
        case "e":
            ret = [
                NodeId(direction="e", x=id.x+1, y=id.y, steps_forward=id.steps_forward+1),
                NodeId(direction="n", x=id.x, y=id.y-1, steps_forward=1),
                NodeId(direction="s", x=id.x, y=id.y+1, steps_forward=1)
            ]
        case "w":
            ret = [
                NodeId(direction="w", x=id.x-1, y=id.y, steps_forward=id.steps_forward+1),
                NodeId(direction="n", x=id.x, y=id.y-1, steps_forward=1),
                NodeId(direction="s", x=id.x, y=id.y+1, steps_forward=1)
            ]
        case "n":
            ret = [
                NodeId(direction="n", x=id.x, y=id.y-1, steps_forward=id.steps_forward+1),
                NodeId(direction="e", x=id.x+1, y=id.y, steps_forward=1),
                NodeId(direction="w", x=id.x-1, y=id.y, steps_forward=1)
            ]
        case "s":
            ret = [
                NodeId(direction="s", x=id.x, y=id.y+1, steps_forward=id.steps_forward+1),
                NodeId(direction="e", x=id.x+1, y=id.y, steps_forward=1),
                NodeId(direction="w", x=id.x-1, y=id.y, steps_forward=1)
            ]

        case _:
            assert(False)

    ret = [n_id for n_id in ret if not (n_id.direction == id.direction and n_id.steps_forward <= id.steps_forward)]

    return [n for n in ret if (n.steps_forward <= 3) and not (n.x < 0 or n.x > len(grid[0])-1 or n.y < 0 or n.y > len(grid)-1)]

initial_id = NodeId(x=0, y=0, direction="e", steps_forward=0)

nodes: dict[NodeId, Node] = {initial_id : Node(visited=False, best=0, heat_loss=0)}

current_id = initial_id

progress = 0
while True:
    neigh_ids = get_neighbors(id=current_id)
    for neigh_id in neigh_ids:
        if not neigh_id in nodes:
            nodes[neigh_id] = Node(visited=False, best=bad_heat_loss, heat_loss=grid[neigh_id.y][neigh_id.x])
        if not nodes[neigh_id].visited:
            cost = 0
            #cost = 0 if (current_id.x == neigh_id.x and current_id.y == neigh_id.y) else nodes[neigh_id].heat_loss            
            if current_id.x != neigh_id.x:
                step = -1 if neigh_id.x > current_id.x else 1
                x = neigh_id.x
                while x != current_id.x:
                    cost = cost + grid[neigh_id.y][x]
                    x = x + step
            if current_id.y != neigh_id.y:
                step = -1 if neigh_id.y > current_id.y else 1
                y = neigh_id.y
                while y != current_id.y:
                    cost = cost + grid[y][neigh_id.x]
                    y = y + step

            nodes[neigh_id].best = min(nodes[neigh_id].best, cost + nodes[current_id].best)
    nodes[current_id].visited = True
    progress = progress + 1
    if progress % 1000 == 0:
        print("progress: ", progress)

    lowest_unvisited_best = bad_heat_loss
    lowest_unvisited_id = None
    for id in nodes.keys():
        if (not nodes[id].visited) and nodes[id].best < lowest_unvisited_best:
            lowest_unvisited_id = id
            lowest_unvisited_best = nodes[id].best
    if lowest_unvisited_id is None:
        break
    current_id = lowest_unvisited_id

end_nodes = [nodes[id] for id in nodes.keys() if id.x == len(grid[0])-1 and id.y == len(grid)-1]
#print(end_nodes)
end_nodes_best = [n.best for n in end_nodes]
#print(end_nodes_best)
print(min(end_nodes_best))

