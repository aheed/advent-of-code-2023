from dataclasses import dataclass
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

def get_triple(line: str) -> list[str]:
    l1 = line.split(" = ")
    l2 = l1[1][1:-1].split(", ")
    return [l1[0], l2[0], l2[1]]

triples = [get_triple(line) for line in lines[2:]]
map = {t[0]: t[1:] for t in triples}


@dataclass
class NodeInLoop:
    cache_key: str
    ends_with_z: bool

@dataclass
class Loop:
    offset: int
    nodes: list[NodeInLoop]

def get_loop(node: str) -> Loop:
    in_index = 0
    total_cnt = 0
    cache:dict[str, int] = {}
    current_node = node
    ret: list[NodeInLoop] = []

    key = node + "0"
    while not key in cache:
        #print(current_nodes)
        current_ends_with_z = current_node[2] == "Z"
        ret.append(NodeInLoop(cache_key=key, ends_with_z=current_ends_with_z))
        cache[key] = total_cnt
        current_node = map[current_node][0 if lines[0][in_index] == "L" else 1]
        in_index = (in_index + 1) % len(lines[0])
        total_cnt = total_cnt + 1
        key = current_node + f"{in_index}"
    return Loop(offset=cache[key], nodes = ret[cache[key]:])

def node_at_z(loop: Loop, index: int) -> NodeInLoop | None:
    if index < loop.offset:
        return None #assumption
    return loop.nodes[(index - loop.offset) % len(loop.nodes)]

def at_z(loop: Loop, index: int) -> bool:
    if n := node_at_z(loop=loop, index=index):
        return n.ends_with_z
    return False

a_nodes = [t[0] for t in triples if t[0][2] == "A"]
#print(a_nodes)

loops = [get_loop(node) for node in a_nodes]
#print(loops)


#################
@dataclass
class ZNode:
    increment: int
    index: int #index into list of ZNode objects
    next_index: int #index into list of ZNode objects

@dataclass
class ZNodeIterator:
    z_nodes: list[ZNode]
    current_index: int

def iterator_from_loop(loop: Loop) -> ZNodeIterator:
    loop_index = 0
    node_index = 0
    z_nodes: list[ZNode] = []
    increment=loop.offset
    while loop_index < len(loop.nodes):
        if loop.nodes[loop_index].ends_with_z:
            z_nodes.append(ZNode(increment=increment, index=node_index, next_index=node_index+1))
            node_index = node_index + 1
            increment = 1
        else:
            increment=increment+1
        loop_index = loop_index + 1
    z_nodes[-1].next_index = 0
    return ZNodeIterator(z_nodes=z_nodes, current_index=0)

def create_iterator(base_iterator: ZNodeIterator, loop: Loop) -> ZNodeIterator:
    cache: dict[str, ZNode] = {}
    z_nodes: list[ZNode] = []
    total_cnt = 0
    base_iterator.current_index = 0
    last_node_total_cnt = 0

    while True:
        current_base_z_node = base_iterator.z_nodes[base_iterator.current_index]    
        total_cnt = total_cnt + current_base_z_node.increment
        base_iterator.current_index = current_base_z_node.next_index

        n = node_at_z(loop=loop, index=total_cnt)
        assert(n)
        if n.ends_with_z:
            key = f"{base_iterator.current_index}" + n.cache_key
            if key in cache:
                cached_node = cache[key]
                z_nodes[-1].next_index = cached_node.index
                break

            new_index = len(z_nodes)
            new_z_node = ZNode(increment=total_cnt - last_node_total_cnt, index=new_index, next_index=new_index+1)
            z_nodes.append(new_z_node)
            cache[key] = new_z_node

    return ZNodeIterator(z_nodes=z_nodes, current_index=0)

iterator = iterator_from_loop(loop=loops[0])
for i in range(1, len(loops)):
    iterator = create_iterator(base_iterator=iterator, loop=loops[i])

print(iterator.z_nodes[0].increment)

