// Benchmark concatenation of slices using append vs using copy

/* Results

$ go test -v -bench . concat_test.go
=== RUN   TestConcatAppend
--- PASS: TestConcatAppend (0.00s)
=== RUN   TestConcatAppendFixed
--- PASS: TestConcatAppendFixed (0.00s)
=== RUN   TestConcatCopy
--- PASS: TestConcatCopy (0.00s)
BenchmarkAppend-4        	20000000	       113 ns/op
BenchmarkAppendFixed-4   	30000000	        48.3 ns/op
BenchmarkCopy-4          	30000000	        47.8 ns/op
PASS
ok  	command-line-arguments	5.373s
*/

package main

import "testing"

var (
	// Test parameters
	x = []int{1, 2}
	y = []int{3}
	z = []int{4, 5}

	// Expected result
	res = []int{1, 2, 3, 4, 5}
)

// concatAppend concatenates slices using built-in append
func concatAppend(slices ...[]int) []int {
	var result []int
	for _, slice := range slices {
		result = append(result, slice...)
	}
	return result
}

// calcSize return the total size of all slices
func calcSize(slices [][]int) int {
	size := 0
	for _, slice := range slices {
		size += len(slice)
	}
	return size
}

// concatAppendFixed concatenates slices using built-in append
func concatAppendFixed(slices ...[]int) []int {
	size := calcSize(slices)
	result := make([]int, 0, size)
	for _, slice := range slices {
		result = append(result, slice...)
	}
	return result
}

// concatCopy concatinates slices using built-in copy
func concatCopy(slices ...[]int) []int {
	size := calcSize(slices)
	result := make([]int, size)

	i := 0
	for _, slice := range slices {
		copy(result[i:], slice)
		i += len(slice)
	}
	return result
}

// eq return true if two slices are equal
func eq(a, b []int) bool {
	if a == nil && b == nil {
		return true
	}

	if a == nil || b == nil {
		return false
	}

	if len(a) != len(b) {
		return false
	}

	for i, v := range a {
		if v != b[i] {
			return false
		}
	}

	return true
}

func TestConcatAppend(t *testing.T) {
	out := concatAppend(x, y, z)
	if !eq(out, res) {
		t.Fatalf("concatAppend - got %v, expected %v\n", out, res)
	}
}

func TestConcatAppendFixed(t *testing.T) {
	out := concatAppend(x, y, z)
	if !eq(out, res) {
		t.Fatalf("concatAppendFixed - got %v, expected %v\n", out, res)
	}
}

func TestConcatCopy(t *testing.T) {
	out := concatCopy(x, y, z)
	if !eq(out, res) {
		t.Fatalf("concatCopy - got %v, expected %v\n", out, res)
	}
}

func BenchmarkAppend(b *testing.B) {
	for i := 0; i < b.N; i++ {
		concatAppend(x, y, z)
	}
}

func BenchmarkAppendFixed(b *testing.B) {
	for i := 0; i < b.N; i++ {
		concatAppendFixed(x, y, z)
	}
}

func BenchmarkCopy(b *testing.B) {
	for i := 0; i < b.N; i++ {
		concatCopy(x, y, z)
	}
}
