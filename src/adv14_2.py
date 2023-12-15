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
    #return ["".join([columns[row_index][column_index] for column_index in range(len(columns[0])) ]) for row_index in range(len(columns), 0, -1)]

columns = [get_column(pattern=lines, pos=p) for p in range(len(lines[0]))]
print(columns)

columns = rotate_cw(columns=columns)
print(columns)

columns = rotate_cw(columns=columns)
columns = rotate_cw(columns=columns)
columns = rotate_cw(columns=columns)
print(columns)

#print(tilt_column(column=columns[0]))
#tilted_columns = [tilt_column(column=column) for column in columns]
#print(tilted_columns)
#column_scores = [column_score(column=column) for column in tilted_columns]
#print(sum(column_scores))
