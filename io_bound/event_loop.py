import asyncio
import argparse
import time
import random
from os import cpu_count

async def simulate_io_bound_task():
    # Simulate an I/O-bound task that takes random time between 0 and 5 seconds
    delay = random.uniform(0, 5)
    # Cannot use time.sleep(delay) as this will block the entire script execution
    # await asyncio.sleep() informs the event loop to run something else while we
    # wait for the sleep to complete
    await asyncio.sleep(delay)
    return delay

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulate I/O-bound tasks with asyncio.")
    max_workers = min(32, cpu_count() + 4)
    parser.add_argument("--tasks", type=int, default=max_workers, help=f"Number of tasks to simulate (default: {max_workers})")
    args = parser.parse_args()

    if args.tasks <= 0:
        print("Number of tasks must be greater than 0.")
        exit(1)

    return args

def summary(args):
    print("Operation Type: I/O Bound Simulation with asyncio (Explicit Event Loop)")
    print(f"Task Count: {args.tasks}")
    print("...")

async def main():
    start_time = time.time()  # Record the start time
    args = parse_arguments()
    summary(args)

    num_tasks = args.tasks

    # Create a list of tasks
    tasks = [simulate_io_bound_task() for _ in range(num_tasks)]

    # Schedule and run tasks concurrently using the event loop
    total_delay = sum(await asyncio.gather(*tasks))

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print(f"Theoretical Synchronous Time: {total_delay:.2f} seconds")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    # Create and run the event loop explicitly
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(main())
    event_loop.close()
