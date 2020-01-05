package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sort"
)

const (
	urlTemplate = "https://api.stocktwits.com/api/2/streams/symbol/%s.json"
)

type count struct {
	symbol string
	count  int
}

// related returns list of related symbols in order
func related(symbol string) ([]count, error) {
	url := fmt.Sprintf(urlTemplate, symbol)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Anonymous structure to get only list of symbols per message
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
			if sym.Symbol != symbol {
				counts[sym.Symbol] += 1
			}
		}
	}

	return sorted(counts), nil
}

// sorted retuns sorted list of <symbol, count> (descending)
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
