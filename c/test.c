#include <stdio.h>

int main() {
  int a = 10;
  int b = 11;

  int *c = &a;
  int *d = &b;

  printf("c=%p *c=%d , (int **)c=%p, *(int **)c=%p, (int *)c=%p, *(int *)c=%d, a=%d, b=%d \n", c, *c, (int **)c, *(int **)c, (int *)c, *(int *)c, a, b );

  *(int **)c = d;
  printf("*(int **)c = d;\n");

  printf("c=%p *c=%d , (int **)c=%p, (int *)c=%p, a=%d, b=%d \n", c, *c, (int **)c, (int *)c, a, b );
  
  return 0;
}
