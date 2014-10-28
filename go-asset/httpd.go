/* httpd that log requests in JSON format */
package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
)

// For Content-Length, calculated on init
var imageLen string

func init() {
	/* image is generated from image.go, see Makefile */
	imageLen = fmt.Sprintf("%d", len(image))
}

// homeHandler serves the image
func homeHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "image/png")
	w.Header().Set("Content-Length", imageLen)
	w.Write(image)
}

func main() {
	port := 8080
	flag.IntVar(&port, "port", port, "port to listen on")
	flag.Parse()

	http.HandleFunc("/", homeHandler)
	addr := fmt.Sprintf(":%d", port)
	log.Fatal(http.ListenAndServe(addr, nil))
}
