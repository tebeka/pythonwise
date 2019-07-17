#include "result.h"

#include <string.h>

const char *result_str(result_t res) {
	return res.sval;
}

double result_float(result_t res) {
	return res.fval;
}

long long result_int(result_t res) {
	return res.ival;
}

void *result_ptr(result_t res) {
	return res.ptr;
}

void set_result_err(result_t *r, const char *err) {
	r->err = strdup(err);
}
