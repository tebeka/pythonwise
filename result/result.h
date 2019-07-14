#ifndef RESULT_H
#define RESULT_H

typedef struct {
  const char *err;
  union {
      const char *sval;
      double fval;
      long long ival;
      void *ptr;
  };
} result_t;

void set_result_err(result_t *r, const char *err);

// Access to union fields from Go
const char *result_str(result_t);
double result_float(result_t);
long long result_int(result_t);
void *result_ptr(result_t);

#endif // RESULT_H
