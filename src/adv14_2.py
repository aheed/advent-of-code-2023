import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

def get_column(pattern: list[str], pos: int) -> str:
    return "".join([line[pos] for line in pattern])

def tilt_column(column: str) -> str:
    no_destination = -1
    destination_pos = no_destination
    chars = list(column)
    main_pos = 0
    while main_pos < len(chars):
        c = chars[main_pos]
        if c == ".":
            if destination_pos == no_destination:
                destination_pos = main_pos
        if c == "#":
            destination_pos = no_destination
        if c == "O":
            if destination_pos != no_destination:
                chars[destination_pos] = "O"
                chars[main_pos] = "."
                main_pos = destination_pos
                destination_pos = no_destination
        main_pos = main_pos + 1
    return "".join(chars)

def column_score(column: str) -> int:
    total = 0
    for i in range(len(column)):
        if column[i] == "O":
            total = total + len(column) - i
    return total

def rotate_cw(columns: list[str]) -> list[str]:
    row_indexes = [row_index for row_index in range(len(columns)-1, -1, -1)]
    return ["".join([columns[column_index][row_index] for column_index in range(len(columns[0])) ]) for row_index in row_indexes]

def get_cache_key(columns: list[str]) -> str:
    return "z".join(columns)

def tilt_columns(columns: list[str]) -> list[str]:
    return [tilt_column(column=column) for column in columns]

def cycle_columns(columns: list[str]) -> list[str]:
    ret = columns
    for _ in range(4):
        ret = tilt_columns(columns=ret)
        ret = rotate_cw(columns=ret)
    return ret

columns = [get_column(pattern=lines, pos=p) for p in range(len(lines[0]))]
#print(columns)

cache: dict[str, int] = {}
iteration = 0
cycle_length = 0 #will be overwritten
while True:
    columns = cycle_columns(columns=columns)
    key = get_cache_key(columns=columns)
    if key in cache:
        cycle_length = iteration - cache[key]
        break
    cache[key] = iteration
    iteration = iteration + 1
#print(iteration, cycle_length)

extra_cycles = ((1000000000-1) - (iteration - cycle_length)) % cycle_length
for _ in range(extra_cycles):
    columns = cycle_columns(columns=columns)

column_scores = [column_score(column=column) for column in columns]
print(sum(column_scores))
