# Exploring Parallel Computing

This repository is designed to provide various benchmarks of how parallelisation techniques across
multiple languages (`python`, `go`, and `node`) respond to simulated CPU and I/O bound workloads.

The purpose of this repository is to show the limitations of parallelisation with certain languages
and to demonstrate that certain parallelisation techniques do not scale well for I/O bound workloads.

## Parallesiation Techniques

- CPU Bound
    - [`python`] ThreadPoolExecutor
    - [`python`] ProcessPoolExecutor
    - [`node`] Worker Threads
    - [`go`] Goroutines
- I/O Bound
    - [`python`] ThreadPoolExecutor
    - [`python`] ProcessPoolExecutor
    - [`python`] Event Loop

## CPU Bound

For the CPU Bound investigations, we will attempt to calculate the mean of a dataset
through a distributed algorithm. This algorithm will split the dataset into `N` chunks
and allocate the work of calculating the sum of the chunk to `N` workers.

### [`python`] ThreadPoolExecutor

```
# By default, the number of thread workers is calculated by a formula
# that is proportional to the number of logical processors made available
# by the machines CPU: min(32, cpu_count() + 4)
python cpu_bound/thread_pool.py

# The number of thread workers can be manually specified by the --workers flag
python cpu_bound/thread_pool.py --workers 32
```

### [`python`] ProcessPoolExecutor

```
# By default, the number of process workers is equal to the number of
# logical processors made available by the machines CPU: cpu_count()
python cpu_bound/process_pool.py

# The number of process workers can be manually specified by the --workers flag
python cpu_bound/process_pool.py --workers 15
```

### [`python`] Worker Threads

```
# By default, the number of workers threads is equal to the number of
# logical processors made available by the machines CPU: require("os").cpus().length
node cpu_bound/workerThread.js

# The number of worker threads can be manually specified by a positional argument
node cpu_bound/workerThread.js 15
```

### [`go`] Goroutines

```
# By default, the number of workers threads is equal to the number of
# logical processors made available by the machines CPU: runtime.NumCPU()
go run cpu_bound/go_routine.go

# The number of go routines can be manually specified by a positional argument
go run cpu_bound/go_routine.go 15
```

## I/O Bound

For the I/O Bound investigations, we will attempt to simulate N tasks
that involve a network request that takes a random period of time between
`0` and `5` seconds to return a response.

For the Process Pool and Thread Pool techniques you can spread the `N` tasks
across a pool of `M` workers. This is not the case for the Event Loop
which always runs on a single thread.

The summary of the I/O bound investigations will include an additional section
`Theoretical Synchronous Time`. This would be the time that it
would have theoretically taken had we executed the tasks synchronously.

### [`python`] ThreadPoolExecutor

```
# By default, the number of thread workers and tasks is calculated by a formula
# that is proportional to the number of logical processors made available
# by the machines CPU: min(32, cpu_count() + 4)
python io_bound/thread_pool.py

# The number of thread workers can be manually specified by the --workers flag
# The number of tasks can be manually specified by the --tasks flag
python io_bound/thread_pool.py --tasks 20 --workers 10
```

### [`python`] ProcessPoolExecutor

```
# By default, the number of process workers and tasks is equal to the number of
# logical processors made available by the machines CPU: cpu_count()
python io_bound/process_pool.py

# The number of thread workers can be manually specified by the --workers flag
# The number of tasks can be manually specified by the --tasks flag
python io_bound/process_pool.py --tasks 20 --workers 10
```

### [`python`] Event Loop

```
# By default, the number of tasks is equal to the number of
# logical processors made available by the machines CPU: cpu_count()
python io_bound/event_loop.py

# The number of tasks can be manually specified by the --tasks flag
python io_bound/process_pool.py --tasks 20
```