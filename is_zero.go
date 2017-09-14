// Check if a value is the zero value for it's type
package main

import (
	"fmt"
	"reflect"
)

// IsZero returns true if val is the zero value for it's type (e.g. 0, 0.0, "", ...)
func IsZero(val interface{}) bool {
	zero := reflect.Zero(reflect.TypeOf(val))
	// We can't use == since it'll panic on maps, slices ...
	return reflect.DeepEqual(zero.Interface(), reflect.ValueOf(val).Interface())
}

func main() {
	// A little test
	var m1 map[int]int
	m2 := map[int]int{1: 2}

	for _, val := range []interface{}{0, 7, "", "hi", m1, m2} {
		fmt.Printf("%v (%T) -> %v\n", val, val, IsZero(val))
	}
}
