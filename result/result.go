package nmath

import (
	"fmt"
	"sync"
	"unsafe"
)

/*
#include <stdlib.h>
#include "result.h"
*/
import "C"

// Result is result from C
type Result struct {
	r    C.result_t
	err  error
	str  *string
	once sync.Once
}

// NewResult returns a new result
func NewResult(r C.result_t) *Result {
	res := Result{r: r}
	if r.err != nil {
		res.err = fmt.Errorf(C.GoString(r.err))
		C.free(unsafe.Pointer(r.err))
	}

	return &res
}

// Err return the result error
func (r *Result) Err() error {
	return r.err
}

// Int return integer value
func (r *Result) Int() int {
	return int(C.result_int(r.r))
}

// Float return float value
func (r *Result) Float() float64 {
	return float64(C.result_float(r.r))
}

// Str returns string
func (r *Result) Str() string {
	r.once.Do(r.getString)
	return *r.str
}

// Ptr returns unsafe.Pointer
func (r *Result) Ptr() unsafe.Pointer {
	return unsafe.Pointer(C.result_ptr(r.r))
}

func (r *Result) getString() {
	cp := C.result_str(r.r)
	if cp == nil {
		*r.str = ""
		return
	}

	*r.str = C.GoString(cp)
	C.free(unsafe.Pointer(cp))
}
