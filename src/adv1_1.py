import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

def get_first_digit(line: str) -> str:
    return next((c for c in line if c.isnumeric()))

print(sum([int(get_first_digit(line) + get_first_digit(line[::-1])) for line in lines]))
