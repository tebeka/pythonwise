package nmath

// #include "nsqrt.h"
import "C"

// Sqrt returns square root of n
func Sqrt(n float64) (float64, error) {
	res := NewResult(C.nsqrt(C.double(n)))
	if err := res.Err(); err != nil {
		return 0, err
	}

	return res.Float(), nil
}
