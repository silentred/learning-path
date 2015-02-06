#include <stdio.h>
#include <limits.h>
#include <float.h>

/* function declaration  */
void func(void);
 
static int count = 5; /* global variable */

int main()
{
   /* my first program in C */
   printf("Hello, World! \n");

   //printf("Storage size for int : %d \n", sizeof(int));

   printf("Minimum float positive value: %E\n", FLT_MIN );
   printf("Maximum float positive value: %E\n", FLT_MAX );
   printf("Precision value: %d\n", FLT_DIG );

   /* variable definition: */
  int a, b;
  int c;
  float f;
 
  /* actual initialization */
  a = 60;
  b = 13;
  
  c = a + b;
  printf("value of c : %d \n", c);

  f = 70.0/3.0;
  printf("value of f : %f \n", f);

	const int LENGTH = 10;
	const int WIDTH = 5;
	const char NEWLINE = '\n';
	int area;  

	area = LENGTH * WIDTH;
	printf("value of area : %d \n", area);
	printf("value of new line: %c", NEWLINE);


	while(count--){
	    func();
	}

	printf("a & b : %d \n", a&b);
	printf("a | b : %d \n", a|b);
	printf("a ^ b : %d \n", a^b);


	int* address = &a;
	printf("address of a : %p\n", address);
   
   return 0;
}


/* function definition */
void func( void )
{
   static int i = 5; /* local static variable */
   i++;

   printf("i is %d and count is %d\n", i, count);
}
