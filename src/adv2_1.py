from dataclasses import dataclass
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

@dataclass
class Game:
    id: int
    subgames: list[dict[str, int]]

max_game = Game(id=0, subgames=[{"red": 12,  "green":13, "blue": 14}])

print(max_game)

def subgame_to_dict(subgame: str) -> dict[str, int]:
    colors: dict[str, int] = {}
    color_strings = subgame.split(",")
    for color_string in color_strings:
        print(color_string)
        kv = color_string.lstrip().split(" ")
        print(kv)
        colors[kv[1]] = int(kv[0])
    return colors

def line_to_game(line: str) -> Game:
    l1 = line.split(":")
    print(l1)
    l2 = l1[1].split(";")
    print(l2)
    #l3_list = [kv.split(" ") for kv in l2]
    subgames = [subgame_to_dict(subgame=sg_string) for sg_string in l2]
    id = int(l1[0].split(" ")[1])
    return Game(id=id, subgames=subgames)

def subgame_is_possible(subgame: dict[str, int]) -> bool:
    return all((subgame[key] <= max_game.subgames[0][key] for key in subgame.keys()))

print(line_to_game(lines[0]))
all_games = [line_to_game(line) for line in lines]
possible_games = [game for game in all_games if all((subgame_is_possible(subgame) for subgame in game.subgames))]
possible_game_ids = [game.id for game in possible_games]
print(possible_game_ids)
print(sum(possible_game_ids))


