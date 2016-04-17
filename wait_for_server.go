package lassie

import (
	"fmt"
	"net/http"
	"time"
)

func waitForServer(URL string, timeout time.Duration) error {
	ch := make(chan bool)
	go func() {
		for {
			_, err := http.Get(URL)
			if err == nil {
				ch <- true
			}
			time.Sleep(10 * time.Millisecond)
		}
	}()

	select {
	case <-ch:
		return nil
	case <-time.After(timeout):
		return fmt.Errorf("server did not reply after %v", timeout)
	}
}
