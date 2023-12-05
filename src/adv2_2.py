from dataclasses import dataclass
import math
import utils

with utils.get_in_file() as infile:
    lines = [line.strip() for line in infile]

@dataclass
class Game:
    id: int
    subgames: list[dict[str, int]]

color_keys = ["red", "green", "blue"]

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

all_games = [line_to_game(line) for line in lines]

def max_needed(color:str, game: Game) -> int:
    return max([subgame.get(color, 0) for subgame in game.subgames])

def game_power(game: Game) -> int:
    return math.prod([max_needed(color=color, game=game) for color in color_keys])

game_powers = [game_power(game) for game in all_games]
print(sum(game_powers))
