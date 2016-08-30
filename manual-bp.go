// "Manual" breapoing in go
// Compile with
//		go build -gcflags "-N -l" hard-bp.go
// Then
//		(gdb) run
// When you hit breakpoint, call "fin" twice to get to the current location
//		(gdb) fin
//		(gdb) fin
// After that it's usuall gdb commands
//		(gdb) p i
//		$1 = 3
package main

import (
	"fmt"
	"syscall"
)

func foo() {
	for i := 0; i < 5; i++ {
		if i == 3 { // Some complicated condition
			// Initiate a breakpoint
			syscall.Kill(syscall.Getpid(), syscall.SIGTRAP)
		}
		fmt.Printf("i = %d\n", i)
	}
}

func main() {
	foo()
}
