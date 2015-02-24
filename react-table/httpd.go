package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
)

func dataHandler(w http.ResponseWriter, r *http.Request) {
	val := r.FormValue("last")
	last, err := strconv.Atoi(val)
	if err != nil {
		last = 0
	}
	size := 10
	items := make([]map[string]string, size)
	for i := 0; i < size; i++ {
		items[i] = map[string]string{
			"name":  fmt.Sprintf("Name %d", i+last),
			"color": fmt.Sprintf("Color %d", i+last),
		}
	}
	enc := json.NewEncoder(w)
	enc.Encode(items)
}

func main() {
	http.HandleFunc("/data", dataHandler)
	fs := http.FileServer(http.Dir("."))
	http.Handle("/", fs)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
