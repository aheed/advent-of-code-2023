import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

steps = lines[0].split(",")
#print(steps[0], steps[-1])

def hash(in_str: str) -> int:
    h = 0
    for c in in_str:
        h = ((h + ord(c)) * 17) % 256
    return h

hashes = [hash(in_str=step) for step in steps]
print(sum(hashes))