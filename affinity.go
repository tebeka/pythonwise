/* CPU affinity in Go */

package main

import (
	"fmt"
	"math/rand"
	"os"
	"runtime"
	"time"
)

/*
#define _GNU_SOURCE
#include <sched.h>
#include <pthread.h>

void lock_thread(int cpuid) {
	pthread_t tid;
	cpu_set_t cpuset;

	tid = pthread_self();
	CPU_ZERO(&cpuset);
	CPU_SET(cpuid, &cpuset);
    pthread_setaffinity_np(tid, sizeof(cpu_set_t), &cpuset);
}
*/
import "C"

func randSleep() {
	time.Sleep(time.Duration(rand.Intn(300)) * time.Millisecond)
}

func setAffinity(cpuID int) {
	runtime.LockOSThread()
	C.lock_thread(C.int(cpuID))
}

func worker(id int, lock bool) {
	if lock {
		setAffinity(id)
	}

	for {
		fmt.Printf("worker: %d, CPU: %d\n", id, C.sched_getcpu())
		randSleep()
	}
}

func main() {
	lock := len(os.Getenv("LOCK")) > 0
	for i := 0; i < runtime.NumCPU(); i++ {
		go worker(i, lock)
	}
	time.Sleep(2 * time.Second)
}
