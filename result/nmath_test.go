package nmath

import (
	"testing"
)

const (
	epsilon = 0.001
)

func abs(v float64) float64 {
	if v < 0 {
		return -v
	}
	return v
}

func TestSqrt(t *testing.T) {
	v, err := Sqrt(2)
	if err != nil {
		t.Fatalf("error in Sqrt(2) - %s", err)
	}
	expected := 1.4142
	if abs(v-expected) > epsilon {
		t.Fatalf("bad value, expected %f, got %f", expected, v)
	}
}

func TestSqrtNeg(t *testing.T) {
	_, err := Sqrt(-2)
	if err == nil {
		t.Fatalf("no error for negative number")
	}
	t.Logf("error: %s", err)
}
