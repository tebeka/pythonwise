package float

import (
	"reflect"
	"strings"
)

const endSymbol = '\x00'

type State func(s string, i int) (int, State, bool)

func startState(s string, i int) (int, State, bool) {
	switch s[i] {
	// "-3"
	case '-':
		return i + 1, signState, true
	// ".2"
	case '.':
		return i + 1, dotState, true
	// "42", "3.14"
	case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
		return i, numState, true
	}
	return 0, nil, false
}

func signState(s string, i int) (int, State, bool) {
	switch s[i] {
	case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
		return i, numState, true
	// ".2"
	case '.':
		return i + 1, dotState, true
	}
	return 0, nil, false
}

func numState(s string, i int) (int, State, bool) {
	switch s[i] {
	case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
		return i + 1, numState, true
	case '.':
		return i + 1, dotState, true
	case endSymbol:
		return i + 1, nil, true
	}
	return 0, nil, false
}

func dotState(s string, i int) (int, State, bool) {
	switch s[i] {
	case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
		return i + 1, decimalState, true
	case endSymbol:
		return i + 1, nil, true
	}
	return 0, nil, false
}

func decimalState(s string, i int) (int, State, bool) {
	switch s[i] {
	case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
		return i + 1, decimalState, true
	case endSymbol:
		return i + 1, nil, true
	}
	return 0, nil, false
}

func (s State) Equal(s2 State) bool {
	v1, v2 := reflect.ValueOf(s), reflect.ValueOf(s2)
	return v1.Pointer() == v2.Pointer()
}

// IsFloat returns true if s is a valid float
// TODO: Support scientific notation (e.g "1e6")
func IsFloat(s string) bool {
	s = strings.TrimSpace(s) + string(endSymbol)
	i, state, ok := 0, State(startState), true
	nDigits := 0
	for i < len(s) {
		i, state, ok = state(s, i)
		if !ok {
			return false
		}
		if state.Equal(numState) || state.Equal(decimalState) {
			nDigits++
		}
	}

	return state == nil && nDigits > 0
}
