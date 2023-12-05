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
    subgames = [subgame for subgame in game.subgames]
    maxes = [subgame.get(color, 0) for subgame in subgames]
    return max(maxes)

    #[max_needed(key) for key in color_keys]
def game_power(game: Game) -> int:
    #return math.mul([m_n[key] for key in m_n := max_needed(subgame).keys])
    return math.prod([max_needed(color=color, game=game) for color in color_keys])

game_powers = [game_power(game) for game in all_games]
print(game_powers)
print(sum(game_powers))
#possible_games = [game for game in all_games if all((subgame_is_possible(subgame) for subgame in game.subgames))]
#possible_game_ids = [game.id for game in possible_games]
#print(sum(possible_game_ids))


