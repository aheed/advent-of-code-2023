import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

def get_triple(line: str) -> list[str]:
    l1 = line.split(" = ")
    l2 = l1[1][1:-1].split(", ")
    return [l1[0], l2[0], l2[1]]

triples = [get_triple(line) for line in lines[2:]]
map = {t[0]: t[1:] for t in triples}

print(map)

total_cnt = 0
in_index = 0
current_code = "AAA"

while current_code != "ZZZ":
    current_code = map[current_code][0 if lines[0][in_index] == "L" else 1]
    in_index = (in_index + 1) % len(lines[0])
    total_cnt = total_cnt + 1

print(in_index)
print(total_cnt)