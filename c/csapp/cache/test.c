#include <stdio.h>

int main(int argc, char const *argv[])
{
    int res;
    res = foo(12);
    printf("%d\n", res);
    return 0;
}

int foo(unsigned int u) {
    return (u > -1) ? 1 : 0;
}