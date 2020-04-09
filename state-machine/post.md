# Functions as State Machine

Let's say you'd like to check is a string is a valid floating point number
(e.g. `"3.14", ".2", "-3.7" ...). One of the common techinques to solve these
kind of problems is to write a [state
machine](https://en.wikipedia.org/wiki/Finite-state_machine).

Here's how the state machine looks like:
![machine](state-machine.png)

Instead of writing the state machine as a single function with a bunch of `if`
statements we're going to write that states as function.

```go
// State is a function that get's the current string and location, and returns
// the next position, next state and error indicator
type State func(s string, i int) (int, State, bool)
```

```go
const endSymbol = '\x00'

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

	return state == nil && nDigits > 0 // need to have at least 1 digit
}
```

Let's see how a state function look like:

```go
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
```


--
- [Valid Number](https://leetcode.com/problems/valid-number/) problem on leetcode
- Lexical Scanning in Go by Rob Pikd
    - [video](https://www.youtube.com/watch?v=HxaD_trXwRE)
    - [slides](https://talks.golang.org/2011/lex.slide)
- 
