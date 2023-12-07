from itertools import product
from pprint import pprint

def get_neighbors(grid, i, j, m, n):
    differences = [-1, 0, 1]

    for di, dj in product(differences, differences):
        ni, nj = i + di, j + dj
        if (ni, nj) == (i, j):
            continue

        if 0 <= ni < m and 0 <= nj < n:
            yield ni, nj

def get_start(grid, i, j):
    while j > 0 and grid[i][j - 1].isalnum():
        j -= 1

    return j

def get_value(grid, i, j):
    k = j
    while k + 1 < len(grid[0]) and grid[i][k + 1].isdigit():
        k += 1

    return int(grid[i][j:k +1])

def gear_ratios_part_1(input_file):
    with open(input_file, "r") as f:
        schematic = [line[:-1] for line in f.readlines()]
        m, n = len(schematic), len(schematic[0])

    part_number_starts = set()
    for i, row in enumerate(schematic):
        for j, item in enumerate(row):
            if not item.isalnum() and item != ".":

                # Pseudo Breadth First Search
                for ni, nj in get_neighbors(schematic, i, j, m, n):
                    if schematic[ni][nj].isdigit():
                        part_number_starts.add((ni, get_start(schematic, ni, nj)))

    return sum([get_value(schematic, i, j) for (i, j) in part_number_starts])

def gear_ratios_part_2(input_file):
    with open(input_file, "r") as f:
        schematic = [line[:-1] for line in f.readlines()]
        m, n = len(schematic), len(schematic[0])

    gear_locations = {}
    for i, row in enumerate(schematic):
        for j, item in enumerate(row):
            if item == "*":
                # Pseudo Breadth First Search
                part_locations = set()
                for ni, nj in get_neighbors(schematic, i, j, m, n):
                    if schematic[ni][nj].isdigit():
                        part_locations.add((ni, get_start(schematic, ni, nj)))

                if len(part_locations) == 2:
                    gear_locations[(i, j)] = [get_value(schematic, i, j) for (i, j) in part_locations]

    return sum([a * b for (a, b) in gear_locations.values()])

example, main = "engine_schematic_example.txt", "engine_schematic_main.txt"
pprint(gear_ratios_part_2(main))