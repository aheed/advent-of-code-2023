import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]


def get_number_set(numbers: str) -> set[int]:
    numbers_list = numbers.strip().split(" ")
    return set([int(n) for n in numbers_list if len(n.strip()) > 0])

def card_matches(line: str) -> int:
    l1 = line.split(":")
    l2 = l1[1].split("|")
    win_set = get_number_set(l2[0])
    my_set = get_number_set(l2[1])
    #print(win_set, my_set, win_set.intersection(my_set))
    return len(win_set.intersection(my_set))

multiplyers = [1 for _ in lines]

for i in range(len(lines)):
    m = multiplyers[i]
    matches = card_matches(lines[i])
    for j in range(i+1, i + matches + 1):
        multiplyers[j] = multiplyers[j] + m

print(sum(multiplyers))
