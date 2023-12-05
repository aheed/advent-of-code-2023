from dataclasses import dataclass
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

@dataclass
class Game:
    id: int
    subgames: list[dict[str, int]]

max_subgame = {"red": 12,  "green":13, "blue": 14}

def subgame_to_dict(subgame: str) -> dict[str, int]:
    colors: dict[str, int] = {}
    color_strings = subgame.split(",")
    for color_string in color_strings:
        kv = color_string.lstrip().split(" ")
        colors[kv[1]] = int(kv[0])
    return colors

def line_to_game(line: str) -> Game:
    l1 = line.split(":")
    l2 = l1[1].split(";")
    subgames = [subgame_to_dict(subgame=sg_string) for sg_string in l2]
    id = int(l1[0].split(" ")[1])
    return Game(id=id, subgames=subgames)

def subgame_is_possible(subgame: dict[str, int]) -> bool:
    return all((subgame[key] <= max_subgame[key] for key in subgame.keys()))

all_games = [line_to_game(line) for line in lines]
possible_games = [game for game in all_games if all((subgame_is_possible(subgame) for subgame in game.subgames))]
possible_game_ids = [game.id for game in possible_games]
print(sum(possible_game_ids))


