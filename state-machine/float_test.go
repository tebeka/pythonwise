package float

import (
	"testing"
)

var testCases = []struct {
	s  string
	ok bool
}{
	{"1", true},
	{"13", true},
	{"1.2", true},
	{".2", true},
	{"2.", true},
	{"-3", true},
	{"-1.2", true},
	{"", false},
	{".", false},
	{"-", false},
}

func TestIsFloat(t *testing.T) {
	for _, tc := range testCases {
		t.Run(tc.s, func(t *testing.T) {
			ok := IsFloat(tc.s)
			if tc.ok != ok {
				t.Errorf("expected %v, got %v", tc.ok, ok)
			}
		})
	}
}
