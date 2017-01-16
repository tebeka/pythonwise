package main

import (
	"C"
	"fmt"
	"sync"
	"time"
)

//export Hi
func Hi(name string) {
	fmt.Printf("Hi %s\n", name)
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			time.Sleep(time.Second)
			fmt.Printf("%d done\n", n)

		}(i)
	}
	wg.Wait()
}

func main() {}
