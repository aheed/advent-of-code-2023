import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

evaluate_cnt = 0
cache: dict[str, int] = {}

def group_fits_at(row: str, pos:int, group: int) -> bool:
    r_len = len(row[pos:])
    if r_len < group:
        return False
    
    if not all((s == "#" or s == "?" for s in row[pos:pos+group])):
        return False
    
    post_group_row = row[pos+group:]
    if not (len(post_group_row) == 0 or post_group_row[0] != "#"):
        return False
    
    pre_group_row = row[:pos]
    if not (len(pre_group_row) == 0 or pre_group_row[-1] != "#"):
        return False
    
    return True

def calc_nof_arrangements(row: str, groups: list[int]) -> int:
    global evaluate_cnt
    global cache
    evaluate_cnt = evaluate_cnt + 1

    key = row + "b" + "c".join([str(n) for n in groups])
    if (r := cache.get(key)) != None:
        return r
    
    if len(groups) == 0:
        return 0 if "#" in row else 1

    last_possible_start_pos = row.index("#")+1 if "#" in row else len(row)
    group0_positions = [i for i in range(last_possible_start_pos) if group_fits_at(row=row, pos=i, group=groups[0])]
    arrs = [calc_nof_arrangements(row=row[i + groups[0]+1:], groups=groups[1:]) for i in group0_positions]
    ret = sum(arrs)
    cache[key] = ret
    return ret

def line_to_row_and_groups(line: str) -> tuple[str, list[int]]:
    row_group = line.split(" ")
    row = row_group[0]
    row = (row + "?") * 4 + row
    groups = [int(n) for n in row_group[1].split(",")]
    groups = groups * 5
    return (row, groups)

rows_and_groups = [line_to_row_and_groups(line=line) for line in lines]

result = [calc_nof_arrangements(row=r_n_g[0], groups=r_n_g[1]) for r_n_g in rows_and_groups]
print(sum(result))
#print(evaluate_cnt)
