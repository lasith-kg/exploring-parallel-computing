const {
  Worker,
  isMainThread,
  parentPort,
  workerData,
} = require("worker_threads");

function calculatePartialSum(start, end) {
  let partialSum = 0;
  for (let i = start; i < end; i++) {
    partialSum += i + 1; // Adding 1 because the range starts at 1, not 0
  }
  return partialSum;
}

function summary(numWorkers) {
  console.log("Operation Type: CPU Bound Simulation with Worker Threads");
  console.log(`Worker Count: ${numWorkers}`);
  console.log("...");
}

if (isMainThread) {
  const start = process.hrtime();

  const data_size = 1000000000;

  // Get the number of workers from a positional argument
  const numWorkers = parseInt(process.argv[2]) || require("os").cpus().length;
  const chunkSize = Math.floor(data_size / numWorkers);

  summary(numWorkers);

  const workerPromises = [];

  for (let i = 0; i < numWorkers; i++) {
    const startIdx = i * chunkSize;
    const endIdx = (i + 1) * chunkSize;

    const workerPromise = new Promise((resolve) => {
      const worker = new Worker(__filename, {
        workerData: { start: startIdx, end: endIdx },
      });

      worker.on("message", (result) => {
        resolve(result);
      });
    });

    workerPromises.push(workerPromise);
  }

  Promise.all(workerPromises).then((partialSums) => {
    const totalSum = partialSums.reduce(
      (sum, partialSum) => sum + partialSum,
      0
    );
    const mean = totalSum / data_size;

    const end = process.hrtime(start);
    const elapsedSeconds = end[0] + end[1] / 1e9;

    console.log(`Mean: ${mean}`);
    console.log(`Elapsed Time: ${elapsedSeconds.toFixed(3)} seconds`);
  });
} else {
  // Worker thread
  const { start, end } = workerData;
  const partialSum = calculatePartialSum(start, end);
  parentPort.postMessage(partialSum);
}
