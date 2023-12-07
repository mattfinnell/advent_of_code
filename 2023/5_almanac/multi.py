from multiprocessing import Pool
from typing import List

import math
import time

def number_stuff(nums, power) -> List[float]:
    start = time.perf_counter()
    results = [math.sqrt(num ** power) for num in nums]
    end = time.perf_counter()

    return results, power, end - start

def number_stuff_wrapper(args):
    return number_stuff(*args)

def parallel_demo(params):
    start_t = time.perf_counter()
    with Pool() as pool:
        results = pool.imap_unordered(number_stuff_wrapper, params)

        for _, power, duration in results:
            print(f"{power} completed in {duration:.2f}s")

    end_t = time.perf_counter()

    print(f"Parallel took {end_t - start_t:.2f}s")

if __name__ == "__main__":
    params = [
        (range(8000000), 3),
        (range(8000000), 4),
        (range(8000000), 5),
        (range(8000000), 6),
        (range(8000000), 7),
        (range(8000000), 8),
        (range(8000000), 9),
        (range(8000000), 10),
    ]

    parallel_demo(params)

    start_t = time.perf_counter()

    for p in params:
        results = number_stuff_wrapper(p)

    end_t = time.perf_counter()

    print(f"Single took {end_t - start_t:.2f}s")