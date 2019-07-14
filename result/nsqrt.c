#include <stddef.h>
#include "result.h"

#define abs(v) (((v) < 0) ? -(v) : (v))
#define ntries 10000

// Calculate sqrt using Newton's method
result_t nsqrt(double n) {
	result_t res;
	res.err = NULL;

	if (n < 0) {
		set_result_err(&res, "sqrt of negative number");
		return res;
	}

	double guess = 1.0;
	double epsilon = 0.00001;
	for (int i = 0; i < ntries; i++) {
		if (abs(guess * guess - n) <= epsilon) {
			res.fval = guess;
			return res;
		}

		guess = (n/guess + guess) / 2.0;
	}

	res.err = "can't find sqrt";
	return res;
}
