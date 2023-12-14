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

def get_reflection_pos(strings: list[str]) -> int | None:
    return next((pos for pos in range(len(strings)-1) if is_reflection_at(strings=strings, pos=pos)), None)

def summarize_pattern(pattern: list[str]) -> int:
    pos = get_reflection_pos(strings=pattern)
    if pos != None:
        return (pos + 1) * 100

    #row_sum = summarize_strings(strings=pattern, multiplier=100)
    columns = [get_column(pattern=pattern, pos=p) for p in range(len(pattern[0]))]
    pos = get_reflection_pos(strings=columns)
    assert(pos != None)
    return pos + 1

    #col_sum = summarize_strings(strings=columns, multiplier=1)
    #return row_sum + col_sum

patterns: list[list[str]] = get_patterns(lines=lines)
#print(patterns)
#print([get_column(pattern=patterns[0], pos=p) for p in range(len(patterns[0][0]))])

#print(summarize_pattern(pattern=patterns[1]))
print(sum([summarize_pattern(pattern=p) for p in patterns]))


