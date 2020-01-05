package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sort"
)

type count struct {
	symbol string
	count  int
}

func related(symbol string) ([]count, error) {
	url := fmt.Sprintf("https://api.stocktwits.com/api/2/streams/symbol/%s.json", symbol)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var reply struct {
		Messages []struct {
			Symbols []struct {
				Symbol string
			}
		}
	}
	dec := json.NewDecoder(resp.Body)
	if err := dec.Decode(&reply); err != nil {
		return nil, err
	}

	counts := make(map[string]int)
	for _, msg := range reply.Messages {
		for _, sym := range msg.Symbols {
			counts[sym.Symbol] += 1
		}
	}

	return sorted(counts), nil

}

func sorted(counts map[string]int) []count {
	arr := make([]count, 0, len(counts))
	for sym, n := range counts {
		arr = append(arr, count{sym, n})
	}

	less := func(i, j int) bool { return arr[i].count > arr[j].count }
	sort.Slice(arr, less)
	return arr
}

func main() {
	counts, err := related("AAPL")
	if err != nil {
		log.Fatal(err)
	}

	for _, c := range counts[:5] {
		fmt.Printf("%-5s % 3d\n", c.symbol, c.count)
	}
}
