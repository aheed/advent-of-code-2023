from dataclasses import dataclass
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]


def extrapolate(history: list[int]) -> int:
    diff_collections: list[list[int]] = []
    
    #done = False
    in_list: list[int] = history
    #in_list = [i for i in history]
    while True:
        diffs = [in_list[i] - in_list[i-1] for i in range(1, len(in_list))]
        diff_collections.append(diffs)
        if all((diff == 0 for diff in diffs)):
            break
        in_list = diffs

    #print(diff_collections)
    diff_collections = [history] + diff_collections
    #print(diff_collections)

    collection_index = len(diff_collections)-1
    while True:
        if collection_index == 0:
            break
        new_value = (diff_collections[collection_index-1])[0] - (diff_collections[collection_index])[0]
        diff_collections[collection_index-1] = [new_value] + diff_collections[collection_index-1]
        collection_index = collection_index - 1
    
    #print(diff_collections)

    return diff_collections[0][0]

hist0 = [int(n) for n in lines[0].split(" ")]
print(hist0)
print(extrapolate(history=hist0))

histories = [[int(n) for n in line.split(" ")] for line in lines]
extrapolations = [extrapolate(history=hist) for hist in histories]
print(extrapolations)

print(sum(extrapolations))
