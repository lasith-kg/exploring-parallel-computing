package main

import (
	"fmt"
	"math"
	"os"
	"runtime"
	"strconv"
	"sync"
	"time"
)

func calculatePartialSum(start int, end int) int {
	var partialSum int = 0
	for i := start; i < end; i++ {
		partialSum += i + 1 // Adding 1 because the range starts at 1, not 0
	}
	return partialSum
}

func parseArguments() int {
	maxWorkers := runtime.NumCPU()
	numWorkers := maxWorkers

	if len(os.Args) > 1 {
		numWorkers = atoi(os.Args[1])
	}

	if numWorkers <= 0 {
		fmt.Println("Number of workers must be greater than 0.")
		os.Exit(1)
	}

	return numWorkers
}

func summary(numWorkers int) {
	fmt.Println("Operation Type: CPU Bound Simulation with Goroutines")
	fmt.Printf("Worker Count: %d\n", numWorkers)
	fmt.Println("...")
}

func atoi(s string) int {
	i, err := strconv.Atoi(s)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	return i
}

func main() {
	startTime := time.Now() // Record the start time

	numWorkers := parseArguments()
	summary(numWorkers)

	dataSize := 1000000000
	chunkSize := int(math.Ceil(float64(dataSize) / float64(numWorkers)))

	var wg sync.WaitGroup
	// partialSums is an array of fixed memory footprint, as
	// its count and memory size of each item is pre-determined
	partialSums := make([]int, numWorkers)

	// Despite the goroutines accessing shared data (partialSums),
	// they are writing to specific index assigned corresponding to the
	// worker number
	// Therefore, this is a thread-safe goroutine as there is no
	// chance of multiple goroutines concurrently writing to the same
	// area of memory
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			start := i * chunkSize
			end := (i + 1) * chunkSize
			partialSum := calculatePartialSum(start, end)
			partialSums[i] = partialSum
		}(i)
	}

	wg.Wait()

	totalSum := 0
	for _, partialSum := range partialSums {
		totalSum += partialSum
	}

	mean := float64(totalSum) / float64(dataSize)

	endTime := time.Now()           // Record the end time
	elapsedTime := endTime.Sub(startTime) // Calculate the elapsed time

	fmt.Printf("Mean: %.2f\n", mean)
	fmt.Printf("Elapsed Time: %.2f seconds\n", elapsedTime.Seconds())
}
