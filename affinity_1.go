/* CPU affinity in Go */

package main

import (
	"fmt"
	"math/rand"
	"runtime"
	"time"
)

/*
#define _GNU_SOURCE
#include <sched.h>
*/
import "C"

func randSleep() {
	time.Sleep(time.Duration(rand.Intn(300)) * time.Millisecond)
}

func worker(id int) {
	for {
		fmt.Printf("worker: %d, CPU: %d\n", id, C.sched_getcpu())
		randSleep()
	}
}

func main() {
	for i := 0; i < runtime.NumCPU(); i++ {
		go worker(i)
	}
	time.Sleep(2 * time.Second)
}
