import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]


def get_patterns(lines: list[str]) -> list[list[str]]:
    next_pattern_start = 0
    ret: list[list[str]] = []

    for n in range(len(lines)):
        if lines[n] == "":
            ret.append(lines[next_pattern_start:n])
            next_pattern_start = n+1

    return ret

def get_column(pattern: list[str], pos: int) -> str:
    return "".join([line[pos] for line in pattern])

def is_reflection_at(strings: list[str], pos: int) -> bool:
    length = min(pos+1, len(strings)-1-pos)
    ret = all((strings[pos-i] == strings[pos+i+1] for i in range(length)))
    return ret

#def summarize_strings(strings: list[str], multiplier: int) -> int:
#    reflection_pos = next((pos for pos in range(len(strings)-1) if is_reflection_at(strings=strings, pos=pos)), None)
#    assert(reflection_pos)
#    return reflection_pos * multiplier

def get_reflection_pos(strings: list[str], exclude_pos: int | None) -> int | None:
    return next((pos for pos in range(len(strings)-1) if is_reflection_at(strings=strings, pos=pos) and not (pos == exclude_pos)), None)

def summarize_pattern(pattern: list[str]) -> int:
    original_reflection_row_pos: int | None = None
    original_reflection_col_pos: int | None = None

    pos = get_reflection_pos(strings=pattern, exclude_pos=None)
    if pos != None:
        original_reflection_row_pos = pos
        #return (pos + 1) * 100
    else:
        columns = [get_column(pattern=pattern, pos=p) for p in range(len(pattern[0]))]
        pos = get_reflection_pos(strings=columns, exclude_pos=None)
        assert(pos != None)
        original_reflection_col_pos = pos
        #return pos + 1

    def smudge(row: int, col: int):
        smudged = "#" if (pattern[row])[col] == "." else "."
        pattern[row] = pattern[row][:col] + smudged + pattern[row][col + 1:]
    
    #smudge_found = False
    for row in range(len(pattern)):
        for col in range(len(pattern[0])):
            smudge(row=row, col=col)

            pos = get_reflection_pos(strings=pattern, exclude_pos=original_reflection_row_pos)
            if pos != None:
                return (pos + 1) * 100
            
            columns = [get_column(pattern=pattern, pos=p) for p in range(len(pattern[0]))]
            pos = get_reflection_pos(strings=columns, exclude_pos=original_reflection_col_pos)
            if pos != None:
                return pos + 1

            smudge(row=row, col=col) #desmudge for next iteration
    assert(False)

patterns: list[list[str]] = get_patterns(lines=lines)
#print(patterns)
#print([get_column(pattern=patterns[0], pos=p) for p in range(len(patterns[0][0]))])

#print(summarize_pattern(pattern=patterns[1]))
print(sum([summarize_pattern(pattern=p) for p in patterns]))


