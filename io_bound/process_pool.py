import concurrent.futures
import argparse
import time
import random
from os import cpu_count

def simulate_io_bound_task():
    # Simulate an I/O-bound task that takes random time between 0 and 5 seconds
    delay = random.uniform(0, 5)
    time.sleep(delay)
    return delay

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulate I/O-bound tasks with ProcessPoolExecutor.")
    max_workers=cpu_count()
    parser.add_argument("--tasks", type=int, default=max_workers, help=f"Number of tasks to simulate (default: {max_workers})")
    parser.add_argument("--workers", type=int, default=max_workers, help=f"Number of workers (default: {max_workers})")
    args = parser.parse_args()

    if args.tasks <= 0:
        print("Number of tasks must be greater than 0.")
        exit(1)

    if args.workers <= 0:
        print("Number of tasks must be greater than 0.")
        exit(1)

    return args

def summary(args):
    print("Operation Type: I/O Bound Simulation with ProcessPoolExecutor")
    print(f"Worker Count: {args.workers}")
    print(f"Task Count: {args.tasks}")
    print("...")

if __name__ == '__main__':
    start_time = time.time()  # Record the start time
    args = parse_arguments()
    summary(args)

    num_tasks = args.tasks
    num_workers = args.workers

    futures = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        for i in range(num_tasks):
            # Simulate I/O-bound tasks concurrently using ProcessPoolExecutor
            future = executor.submit(simulate_io_bound_task)
            futures.append(future)
        
        partial_delays = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Calculate statistics
    total_delay = sum(partial_delays)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print(f"Theoretical Synchronous Time: {total_delay:.2f} seconds")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")
