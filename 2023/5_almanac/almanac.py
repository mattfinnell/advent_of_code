from collections import deque
from multiprocessing import Pool
from pprint import pprint
from typing import List

import time
import math

class IntervalMapping:
    def __init__(self, source, dest, range):
        self.source_start = source
        self.source_end = source + range - 1

        self.dest_start = dest
        self.dest_end = dest + range - 1

        self.difference = self.dest_start - self.source_start
        self.range = range

    def map(self, key):
        return key + self.difference

    def __repr__(self):
        return f"IntervalMapping [{self.difference}] ({self.source_start}, {self.source_end}) --> ({self.dest_start}, {self.dest_end})"

def read_tables(lines):
    raw_tables = []
    for line in lines:
        if line == "\n":
            raw_tables.append([])

        elif line[0].isdigit():
            raw_tables[-1].append([int(value) for value in line.split(" ")])

    tables = []
    for table in raw_tables:
        new_table = []
        for dest, source, range in table:
            new_table.append(IntervalMapping(source, dest, range))

        tables.append(sorted(new_table, key=lambda x: x.source_start))

    return tables

def read_file_part_1(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    seeds = [
        int(value) 
        for value in filter(lambda x: x != "", lines[0].split(":")[1].split(" "))
    ]

    return seeds, read_tables(lines[1:])

def read_file_part_2(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    raw = deque([
        int(value) 
        for value in filter(lambda x: x != "", lines[0].split(":")[1].split(" "))
    ])

    seed_ranges = []
    while raw:
        start, n = raw.popleft(), raw.popleft()
        seed_ranges.append((start, start + n - 1))

    return sorted(seed_ranges, key=lambda x: x[0]), read_tables(lines[1:])

def check_intervals(tables):
    # Interval overlap checking
    for table in tables:
        source_intervals = [(source, source + range - 1) for (_, source, range) in table]
        dest_intervals = [(dest, dest + range - 1) for (dest, _, range) in table]

        source_intervals, dest_intervals = sorted(source_intervals), sorted(dest_intervals)

        for intervals in [source_intervals, dest_intervals]:
            for (_, end), (start, __) in zip(intervals[:-1], intervals[1:]):
                if start <= end:
                    print(f"Overlap Detected: {start} <= {end}")
                    return False

    return True

def translate(seed, tables: List[List[IntervalMapping]]) -> int:
    input = seed
    for table in tables:
        for interval in table:
            if interval.source_start <= input <= interval.source_end:
                input = interval.map(input)
                break

    return input

def almanac_part_1(input_file):
    seeds, tables = read_file_part_1(input_file)

    locations = { seed: translate(seed, tables) for seed in seeds }

    return min(locations.values())

def almanac_part_2_brute_force(input_file):
    (seed_ranges, tables), minimum = read_file_part_2(input_file), math.inf

    count, total = 0, sum((b - a + 1) for (a, b) in seed_ranges)

    time_start, time_granularity = time.perf_counter(), 10000000 # 1 Million
    for i, (a, b) in enumerate(seed_ranges):
        print(f"range {i} ({a}, {b}) @{b - a + 1} seeds")
        for seed in range(a, b + 1):
            minimum = min(minimum, translate(seed, tables))
            count += 1

            if count % time_granularity == 0:
                time_delta = time.perf_counter() - time_start
                print(f"{count} - {time_delta} for {time_granularity} Seeds")
                time_start = time.perf_counter()

    return minimum

def almanac_part_2_inverses(input_file):
    (seed_ranges, tables), minimum = read_file_part_2(input_file), math.inf

    # Construct inverse tables
    inversed_tables = []
    for table in reversed(tables):
        inversed_table = []
        for interval in table:
            inversed_table.append(
                IntervalMapping(
                    interval.dest_start, 
                    interval.source_start, 
                    interval.range
                )
            )

        inversed_tables.append(inversed_table)

    # Reverse feed the output ranges to get input ranges
    candidates = []
    for interval in inversed_tables[0]:
        seed = min(
            translate(interval.dest_start, inversed_tables), 
            translate(interval.dest_end, inversed_tables)
        )

        for low, high in seed_ranges:
            if low <= seed <= high:
                candidates.append(seed)

    return min(candidates)

def compute_min_seed(low, high, tables) -> int:
    start_time = time.perf_counter()

    minimum = math.inf
    for seed in range(low, high + 1):
        minimum = min(minimum, translate(seed, tables))

    end_time = time.perf_counter()

    return minimum, (high - low + 1), end_time - start_time

def compute_min_seed_wrapper(params) -> int:
    return compute_min_seed(*params)

def chunk_range(low, high, n):
    result, current = [], low

    while current + n <= high:
        result.append((current, current + n))
        current = current + n + 1

    if current <= high:
        result.append((current, high))

    return result

def almanac_part_2_parallel(input_file):
    (seed_ranges, tables) = read_file_part_2(input_file)

    ranges = []
    for low, high in seed_ranges:
        ranges.extend(chunk_range(low, high, 1_000_000))

    process_parameters = [(low, high, tables) for (low, high) in ranges]

    with Pool() as pool:
        results = pool.imap_unordered(compute_min_seed_wrapper, process_parameters)

        for _, n, time in results:
            pprint(f"Processed {n} results in {time:.2f} seconds")

    return min([result[0] for result in results]) 

def almanac_things(input_file):
    (seed_ranges, tables) = read_file_part_2(input_file)

    n_seeds = sorted([(b - a + 1) / 1000000 for (a, b) in seed_ranges])

    return n_seeds

main, example = "almanac_main.txt", "almanac_example.txt"

# pprint(almanac_part_2_brute_force(example)) # 5 Hours - 84206669  ...holy shit lol
pprint(almanac_part_2_parallel(main)) # 1.5 Hours

# pprint(almanac_things(main))
