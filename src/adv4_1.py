import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]


def get_number_set(numbers: str) -> set[int]:
    numbers_list = numbers.strip().split(" ")
    return set([int(n) for n in numbers_list if len(n.strip()) > 0])

def card_score(line: str) -> int:
    l1 = line.split(":")
    l2 = l1[1].split("|")
    win_set = get_number_set(l2[0])
    my_set = get_number_set(l2[1])
    nof_matching = len(win_set.intersection(my_set))
    return pow(base=2, exp=nof_matching-1) if nof_matching > 0 else 0
    
print(sum([card_score(line) for line in lines]))
