from enum import Enum
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

"""
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
"""

def get_min_row(groups: list[int]) -> str:
    chars = ["#" * n for n in groups]
    return ".".join(chars)

def get_candidates(row: str, groups: list[int]) -> list[str]:
    if len(groups) == 0:
        return []
    min_group_len = sum(groups) + len(groups) - 1
    max_space = len(row) - min_group_len
    min_row = get_min_row(groups=groups)
    ret = [("." * space) + min_row for space in range(max_space+1)]
    for space in range(max_space):
        ret = ret + ["." * space + "#" * groups[0] + "." + cand for cand in get_candidates(row=row[space + groups[0] + 1:], groups=groups[1:])]
    ret = [r + "." * (len(row) - len(r)) for r in ret]
    return ret
    #return ["#" + get_candidates(row=row[space:], groups=groups[1:]) for space in range(max_space)]

#def calc_nof_arrangements(row: str, groups: list[int]) -> int:
    
def row_fits(given_row: str, candidate_row: str) -> bool:
    assert(len(given_row) == len(candidate_row))

    for i in range(len(given_row)):
        c = candidate_row[i]
        r = given_row[i]        
        if r != "?" and c != r:
            return False

    return True

def get_arrangements(row: str, groups: list[int]) -> list[str]:
    candidates = get_candidates(row=row, groups=groups)
    return [cand for cand in candidates if row_fits(given_row=row, candidate_row=cand)]

def line_to_row_and_groups(line: str) -> tuple[str, list[int]]:
    row_group = line.split(" ")
    #row = [char_to_status(c=c) for c in row_group[0]]
    groups = [int(n) for n in row_group[1].split(",")]
    return (row_group[0], groups)

rows_and_groups = [line_to_row_and_groups(line=line) for line in lines]
print(rows_and_groups[0])

#print(calc_nof_arrangements(row=rows_and_groups[-1][0], groups=rows_and_groups[-1][1]))
#print([calc_nof_arrangements(row=r_n_g[0], groups=r_n_g[1]) for r_n_g in rows_and_groups])
#print(sum([calc_nof_arrangements(row=r_n_g[0], groups=r_n_g[1]) for r_n_g in rows_and_groups]))

#test = line_to_row_and_groups("???? 2,1")
#print(calc_nof_arrangements(row=test[0], groups=test[1]))

# 9241 is too high
# 6434 is too low
# 7735 is wrong

def print_rows(rows: list[str]):
    for row in rows:
        print(row)
    print("")


#r_n_g = rows_and_groups[0]
#cand = get_candidates(row=r_n_g[0], groups=r_n_g[1])
#print_rows(cand)

cands = [get_candidates(row=r_n_g[0], groups=r_n_g[1]) for r_n_g in rows_and_groups]
#[print_rows(cand) for cand in cands]

#print("--------")
arrangements = [get_arrangements(row=r_n_g[0], groups=r_n_g[1]) for r_n_g in rows_and_groups]
arrangements = [list(set(a)) for a in arrangements] #remove duplicates
#[print_rows(a) for a in arrangements]
arr_lengths = [len(arr) for arr in arrangements]
print(arr_lengths)
print(sum(arr_lengths)) #yields 7286 which is the correct answer for 12_1