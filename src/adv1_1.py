import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

print(lines)