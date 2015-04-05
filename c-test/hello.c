/*
#include "stdio.h"

int main(void){
	printf("%s\n", "Hello World. \n");
	return 0;
}


#include <math.h>
#include <stdio.h>

int main(void)
{
	double pi = 3.1416;
	printf("sin(pi/2)=%f\nln1=%f\n", sin(pi/2), log(1.0));
	return 0;
}

#include <stdio.h>

int hour = 23, minute=59;
int x =10;

void print_time(void){
	printf("%d:%d in print_time\n", hour, minute);
}

int main(void)
{
	int hour = 0, minute=30;
	print_time();
	printf("%d:%d in main\n", hour, minute);
	printf("x=%d \n", x);
	return 0;
}



#include <stdio.h>
void foo(void)
{
	int i;
	printf("%d\n", i);
	i = 777;
}

int main(void)
{
	foo();
	printf("hello\n");
	foo();
	return 0;
}
*/

#include <stdio.h>
void foo(void)
{
	int i = 0;
	{
		int i = 1;
		int j = 2;
		printf("i=%d, j=%d\n", i, j);
	}
	printf("i=%d\n", i); /* cannot access j here */
}
int main(void)
{
	foo();
	return 0;
}