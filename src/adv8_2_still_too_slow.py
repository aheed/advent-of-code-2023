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

#print(map)

@dataclass
class Loop:
    offset: int
    ends_with_z: list[bool]

def get_loop(node: str) -> Loop:
    in_index = 0
    total_cnt = 0
    cache:dict[str, int] = {}
    current_node = node
    ret: list[bool] = []

    #key = node + f"{in_index}"
    key = node + "0"
    while not key in cache:
        #print(current_nodes)
        current_ends_with_z = current_node[2] == "Z"
        ret.append(current_ends_with_z)
        cache[key] = total_cnt
        current_node = map[current_node][0 if lines[0][in_index] == "L" else 1]
        in_index = (in_index + 1) % len(lines[0])
        total_cnt = total_cnt + 1
        key = current_node + f"{in_index}"
    return Loop(offset=cache[key], ends_with_z=ret[cache[key]:])

def at_z(loop: Loop, index: int) -> bool:
    if index < loop.offset:
        return False #assumption
    return loop.ends_with_z[(index - loop.offset) % len(loop.ends_with_z)]

total_cnt = 0
in_index = 0
current_nodes = [t[0] for t in triples if t[0][2] == "A"]
print(current_nodes)

loops = [get_loop(node) for node in current_nodes]
print(loops)

while not all((at_z(loop, total_cnt) for loop in loops)):
    total_cnt = total_cnt + 1
    if total_cnt % 100000 == 0:
        print(total_cnt)

#while not all((node[2] == "Z" for node in current_nodes)):
#    #print(current_nodes)
#    current_nodes = [ map[node][0 if lines[0][in_index] == "L" else 1] for node in current_nodes]
#    in_index = (in_index + 1) % len(lines[0])
#    total_cnt = total_cnt + 1

##print(in_index)
print(total_cnt)