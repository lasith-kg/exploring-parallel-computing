import concurrent.futures
import argparse
import time
from os import cpu_count

def calculate_partial_sum(start, end):
    partial_sum = 0
    for i in range(start, end):
        partial_sum += i + 1  # Adding 1 because the range starts at 1, not 0
    return partial_sum

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulate CPU-bound tasks with ProcessPoolExecutor.")
    max_workers=cpu_count()
    parser.add_argument("--workers", type=int, default=max_workers, help=f"Number of worker (default: {max_workers})")
    args = parser.parse_args()

    if args.workers <= 0:
        print("Number of workers must be greater than 0.")
        exit(1)

    return args

def summary(args):
    print("Operation Type: CPU Bound Simulation with ProcessPoolExecutor")
    print(f"Worker Count: {args.workers}")
    print("...")

if __name__ == '__main__':
    start_time = time.time()  # Record the start time

    args = parse_arguments()
    summary(args)

    data_size = 1000000000
    num_workers = args.workers
    chunk_size = data_size // num_workers

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for i in range(num_workers):
            start = i * chunk_size
            end = (i + 1) * chunk_size
            future = executor.submit(calculate_partial_sum, start, end)
            futures.append(future)

        partial_sums = [future.result() for future in concurrent.futures.as_completed(futures)]

    total_sum = sum(partial_sums)
    mean = total_sum / data_size

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print(f"Mean: {mean}")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")