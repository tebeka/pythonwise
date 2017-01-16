#include "hi.h"
#include <stdio.h>

int
main() {
    printf("C starts\n");
    GoString name = { "Daffy", 5 };
    Hi(name);
    printf("C ends\n");
    return 0;
}
