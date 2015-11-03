package main

import (
    "fmt"
    "runtime"
    "sync"
)

// Possible worker states.
const (
    Stopped = 0
    Paused  = 1
    Running = 2
)

// Maximum number of workers.
const WorkerCount = 10

func main() {
    // Launch workers.
    var wg sync.WaitGroup
    wg.Add(WorkerCount + 1)

    workers := make([]chan int, WorkerCount)
    for i := range workers {
        workers[i] = make(chan int, 1)

        go func(i int) {
            worker(i, workers[i])
            wg.Done()
        }(i)
    }

    // Launch controller routine.
    go func() {
        controller(workers)
        wg.Done()
    }()

    // Wait for all goroutines to finish.
    wg.Wait()
}

func worker(id int, ws <-chan int) {
    state := Paused // Begin in the paused state.

    for {
        select {
        case state = <-ws:
            switch state {
            case Stopped:
                fmt.Printf("Worker %d: Stopped\n", id)
                return
            case Running:
                fmt.Printf("Worker %d: Running\n", id)
            case Paused:
                fmt.Printf("Worker %d: Paused\n", id)
            }

        default:
            // We use runtime.Gosched() to prevent a deadlock in this case.
            // It will not be needed of work is performed here which yields
            // to the scheduler.
            runtime.Gosched()

            if state == Paused {
                break
            }

            // Do actual work here.
        }
    }
}

// controller handles the current state of all workers. They can be
// instructed to be either running, paused or stopped entirely.
func controller(workers []chan int) {
    // Start workers
    setState(workers, Running)

    // Pause workers.
    setState(workers, Paused)

    // Unpause workers.
    setState(workers, Running)

    // Shutdown workers.
    setState(workers, Stopped)
}

// setState changes the state of all given workers.
func setState(workers []chan int, state int) {
    for _, w := range workers {
        w <- state
    }
}