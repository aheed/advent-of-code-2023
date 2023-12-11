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

total_cnt = 0
in_index = 0
current_nodes = [t[0] for t in triples if t[0][2] == "A"]

while not all((node[2] == "Z" for node in current_nodes)):
    #print(current_nodes)
    current_nodes = [ map[node][0 if lines[0][in_index] == "L" else 1] for node in current_nodes]
    in_index = (in_index + 1) % len(lines[0])
    total_cnt = total_cnt + 1

#print(in_index)
print(total_cnt)