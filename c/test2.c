#include <stdio.h>
#include <limits.h>
#include <float.h>

/* function declaration  */
void binary_(int x);
 
static int count = 5; /* global variable */


int main()
{
   /* my first program in C */
   printf("Hello, World! \n");
   printf("SCHAR_MIN, SCHAR_MAX, SCHAR_MAX:%d, %d, %d . \n",SCHAR_MIN, SCHAR_MAX, SCHAR_MAX);
   printf("SHRT_MIN, SHRT_MAX, SHRT_MAX:%d, %d, %d . \n",SHRT_MIN, SHRT_MAX, SHRT_MAX);
   printf("INT_MIN, INT_MAX, UINT_MAX:%d, %d, %d . \n",INT_MIN, INT_MAX, UINT_MAX);
   printf("LONG_MIN, LONG_MAX, LONG_MAX:%ld, %ld, %ld . \n",LONG_MIN, LONG_MAX, LONG_MAX);
   printf("%d \n", '\60');

   char *msg = "hello world"; //msg是指向第一个字符“h”的指针；这里是对msg赋值而不是对*msg赋值，和下面的例子等价。
   printf("char:%c point: %p\n",*(msg+1), msg);

   //上面的方式容易让人误解，以为"hello"赋给了*msg，其实不是的，"hello"赋给了msg。
   char *message;
   message = "Hello !!!";  //message是字符指针，字符串字面量的直接值也是指针，所以可以这样赋值；
   printf("char:%s point: %p\n",message, message);

   /*int a = 48; 这里win下编译通过，但是执行出错
   printf("string is %s\n", a);*/

   printf("%d\n", EOF);

   int x;
   x = 70+3;
   printf("%d\n", ~x);

   return 0;
}

void binary_(int x)
{
    if (x<=0) return;
    else
    {           
        binary_(x/2);
        printf("%d",x%2);
    }
}
