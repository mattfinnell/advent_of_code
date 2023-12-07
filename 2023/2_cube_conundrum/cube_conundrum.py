from functools import reduce
from collections import namedtuple
from typing import List, Dict
from pprint import pprint

MaxCubes = namedtuple("MaxCubes", ["red", "green", "blue"])

def parse_round(round: List[str]):
    counter = {"red": 0, "green": 0, "blue": 0}

    for cube in round:
        cube_type, cube_count = (
            ''.join(filter(lambda x: x.isalpha(), cube)),
            int(''.join(filter(lambda x: x.isdigit(), cube))),
        )

        counter[cube_type] = cube_count

    return counter 

def parse_line(line: str) -> List[List[Dict[str, int]]]:
    rounds = [parse_round(round.split(",")) for round in line.split(":")[1].split(";")]

    return rounds

def is_game_valid(game: List[Dict[str, int]], max_cubes: MaxCubes) -> bool: 
    for round in game:
        for color, count in round.items():
            if count > max_cubes._asdict()[color]:
                return False

    return True

def cube_conundrum_part_1(input_file, max_cubes: MaxCubes):
    with open(input_file, "r") as f:
        games = [parse_line(line) for line in f.readlines()]

    score = 0
    for i, game in enumerate(games):
        if is_game_valid(game, max_cubes):
            score += i + 1

    return score

def cube_conundrum_part_2(input_file, max_cubes: MaxCubes):
    with open(input_file, "r") as f:
        games = [parse_line(line) for line in f.readlines()]

    game_results = []
    for game in games:
        max_visited = {"red": 0, "green": 0, "blue": 0}

        for round in game:
            for color, count in round.items():
                max_visited[color] = max(max_visited[color], count)
        
        game_results.append(max_visited)

    return sum([
        reduce(lambda a, b: a * b, game_result.values(), 1)
        for game_result in game_results
    ])

example, main_part_1 = "example.txt", "part_1.txt"

result = cube_conundrum_part_2(main_part_1, MaxCubes(12, 13, 14)) 

pprint(result)