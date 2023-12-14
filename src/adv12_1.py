import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

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
    return [r + "." * (len(row) - len(r)) for r in ret]
    
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
    arrs = [cand for cand in candidates if row_fits(given_row=row, candidate_row=cand)]
    arrs = list(set(arrs)) #remove duplicates
    return arrs

def line_to_row_and_groups(line: str) -> tuple[str, list[int]]:
    row_group = line.split(" ")
    groups = [int(n) for n in row_group[1].split(",")]
    return (row_group[0], groups)

rows_and_groups = [line_to_row_and_groups(line=line) for line in lines]

def print_rows(rows: list[str]):
    for row in rows:
        print(row)
    print("")


#r_n_g = rows_and_groups[1]
#print(r_n_g)
#arrs = get_arrangements(row=r_n_g[0], groups=r_n_g[1])
#print_rows(arrs)

arrangements = [get_arrangements(row=r_n_g[0], groups=r_n_g[1]) for r_n_g in rows_and_groups]
arr_lengths = [len(arr) for arr in arrangements]

print(sum(arr_lengths))