// HTTP proxy that strips headers from the backend response
package main

import (
	"flag"
	"fmt"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"strings"
)

// StripTransport strips headers from backend response
type StripTransport struct {
	http.RoundTripper
	headers map[string]bool
}

// RoundTrip handles request, then removes headers from the response
func (lt *StripTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	resp, err := lt.RoundTripper.RoundTrip(req)
	if err != nil {
		return nil, err
	}

	for hdr := range resp.Header {
		if lt.headers[strings.ToUpper(hdr)] {
			resp.Header.Del(hdr)
		}
	}

	return resp, nil
}

// parseHeaders creates a dictionary where keys are headers in uppercase
func parseHeaders(items []string) map[string]bool {
	out := make(map[string]bool)
	for _, item := range items {
		out[strings.ToUpper(item)] = true
	}
	return out
}

func main() {
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "usage: %s PROXY_URL [HEADER [HEADER ...]]\n", os.Args[0])
		flag.PrintDefaults()
	}
	port := flag.Int("port", 8080, "proxy port (8080)")
	flag.Parse()

	if flag.NArg() < 1 {
		fmt.Fprintf(os.Stderr, "error: wrong number of arguments\n")
		os.Exit(1)
	}

	target, err := url.Parse(flag.Arg(0))
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: bad proxy url - %s\n", err)
		os.Exit(1)
	}

	proxy := &httputil.ReverseProxy{
		Transport: &StripTransport{
			http.DefaultTransport,
			parseHeaders(flag.Args()[1:]), // First argument is proxy URL
		},
		Director: func(r *http.Request) {
			r.URL.Scheme = target.Scheme
			r.URL.Host = target.Host
		},
	}
	http.Handle("/", proxy)
	http.ListenAndServe(fmt.Sprintf(":%d", *port), nil)
}
