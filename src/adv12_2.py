from enum import Enum
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

evaluate_cnt = 0
cache: dict[str, int] = {}

class Status(Enum):
    UNKNOWN = 1
    YES = 2
    NO = 3

def group_fits_at(row: list[Status], pos:int, group: int) -> bool:
    r_len = len(row[pos:])
    if r_len < group:
        return False
    
    if not all((s == Status.YES or s == Status.UNKNOWN for s in row[pos:pos+group])):
        return False
    
    post_group_row = row[pos+group:]
    if not (len(post_group_row) == 0 or post_group_row[0] != Status.YES):
        return False
    
    pre_group_row = row[:pos]
    if not (len(pre_group_row) == 0 or pre_group_row[-1] != Status.YES):
        return False
    
    return True

def calc_nof_arrangements(row: list[Status], groups: list[int]) -> int:
    global evaluate_cnt
    global cache
    evaluate_cnt = evaluate_cnt + 1

    key = "a".join([str(c) for c in row]) + "b" + "c".join([str(n) for n in groups])
    if (r := cache.get(key)) != None:
        return r
    
    if len(groups) == 0:
        return 0 if Status.YES in row else 1

    last_possible_start_pos = row.index(Status.YES)+1 if Status.YES in row else len(row)
    group0_positions = [i for i in range(last_possible_start_pos) if group_fits_at(row=row, pos=i, group=groups[0])]
    arrs = [calc_nof_arrangements(row=row[i + groups[0]+1:], groups=groups[1:]) for i in group0_positions]
    ret = sum(arrs)
    cache[key] = ret
    return ret

def char_to_status(c: str) -> Status:
    match c:
        case "?":
            return Status.UNKNOWN
        case "#":
            return Status.YES
        case ".":
            return Status.NO
        case _:
            assert(False)

def line_to_row_and_groups(line: str) -> tuple[list[Status], list[int]]:
    row_group = line.split(" ")
    row = [char_to_status(c=c) for c in row_group[0]]
    row = (row + [Status.UNKNOWN]) * 4 + row
    groups = [int(n) for n in row_group[1].split(",")]
    groups = groups * 5
    return (row, groups)

rows_and_groups = [line_to_row_and_groups(line=line) for line in lines]

result = [calc_nof_arrangements(row=r_n_g[0], groups=r_n_g[1]) for r_n_g in rows_and_groups]
print(sum(result))
#print(evaluate_cnt)
