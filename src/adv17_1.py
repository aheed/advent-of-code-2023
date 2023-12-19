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

    return [n for n in ret if (n.steps_forward <= 3) and not (n.x < 0 or n.x > len(grid[0])-1 or n.y < 0 or n.y > len(grid)-1)]

initial_id = NodeId(x=0, y=0, direction="e", steps_forward=0)
unvisited_nodes: dict[NodeId, Node] = {initial_id : Node(best=0, heat_loss=0)}
visited_nodes: dict[NodeId, Node] = {}

current_id = initial_id

progress = 0
while True:
    neigh_ids = get_neighbors(id=current_id)
    for neigh_id in neigh_ids:
        if not neigh_id in visited_nodes:            
            if not neigh_id in unvisited_nodes:
                unvisited_nodes[neigh_id] = Node(best=bad_heat_loss, heat_loss=grid[neigh_id.y][neigh_id.x])

            cost = 0 if (current_id.x == neigh_id.x and current_id.y == neigh_id.y) else unvisited_nodes[neigh_id].heat_loss 
            unvisited_nodes[neigh_id].best = min(unvisited_nodes[neigh_id].best, cost + unvisited_nodes[current_id].best)
    
    unvisited_nodes[current_id].visited = True
    visited_nodes[current_id] = unvisited_nodes[current_id]
    unvisited_nodes.pop(current_id)
    
    progress = progress + 1
    if progress % 1000 == 0:
        print("progress: ", progress)

    if len(unvisited_nodes) == 0:
        break

    lowest_unvisited_id, _ = min(unvisited_nodes.items(), key=lambda n: n[1].best)
    current_id = lowest_unvisited_id

end_nodes = [visited_nodes[id] for id in visited_nodes.keys() if id.x == len(grid[0])-1 and id.y == len(grid)-1]
end_nodes_best = [n.best for n in end_nodes]
print(min(end_nodes_best))
