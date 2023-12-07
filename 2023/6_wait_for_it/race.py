from functools import reduce
from pprint import pprint
from typing import List, Tuple

def read_file(input_file: str) -> List[Tuple[int, int]]:
    with open(input_file, "r") as f:
        lines = [list(filter(lambda x: x != "", line[:-1].split(":")[1].split(" "))) for line in f.readlines()]

    times, distances = [int(item) for item in lines[0]], [int(item) for item in lines[1]]

    return list(zip(times, distances))

def get_win_combinations(time, record_distance):
        wins = 0
        for velocity in range(1, time + 1):
            distance = velocity * (time - velocity)

            if distance > record_distance: 
                wins += 1
        
        return wins

def race_part_1(input_file):
    records = read_file(input_file)

    win_combinations = [] 
    for time, record_distance in records:
        win_combinations.append(get_win_combinations(time, record_distance))
    
    pprint(win_combinations)
    return reduce(lambda a, b: a * b, win_combinations, 1)

example, main = "race_example.txt", "race_main.txt"

pprint(race_part_1(example))
pprint(race_part_1(main))