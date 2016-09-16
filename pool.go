// Pool in go using buffer channels
package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// worker simulates work of a goroutine
func worker(id int, pool chan int, start chan bool, wg *sync.WaitGroup) {
	<-start                        // Wait for all goroutines
	rsc := <-pool                  // Get item from the pool
	defer func() { pool <- rsc }() // Return item at end
	defer wg.Done()                // Signal we're dong

	time.Sleep(time.Duration(rand.Int()%100) * time.Millisecond)
	fmt.Printf("worker %d got resource %d\n", id, rsc)
}

func main() {
	var wg sync.WaitGroup
	start := make(chan bool)

	// Create and fill pool
	pool := make(chan int, 3)
	for i := 0; i < 3; i++ {
		pool <- i
	}

	// Run workers
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go worker(i, pool, start, &wg)
	}

	close(start) // Signal to start
	wg.Wait()    // Wait for goroutines to finish before exiting
}
