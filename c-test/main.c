#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(int argc, char *argv[])
{
    //int strLen(char *s);
    int len = strlen("ccc");
    printf("Hello world!\n");
    printf("string length is %d \n", len);

    int heap[6] = {1,2,3,4,5,6};
    int x = 3;
    int result;
    //result = binSearch(x, heap, sizeof(heap));
    //printf("Index is %d", result);

    int twoSum(int numbers[], int n, int target);
    int num[4] = {3,2,4};
    len = sizeof(num)/sizeof(int);
    twoSum(num, len, 6);

    void reverse();
    char s[] = "hello world";
    reverse(s);
    printf("\n revered is %s\n", s);

    if(3 - sizeof(int)){
        printf("int \n");
    }else{
        printf("unsigned int \n");
    }

    int a[4] = {4,5,6,7}, *pa = a;
    printf("*pa is a[0]: %d\n", *pa);
    printf("*(pa+1) is %d\n", *(pa+1));
    printf("a[2] is %d\n", *(a+2));
    printf("pointer of a is %p\n", a);
    printf("a[5], out of range : %d\n", *(pa+5) );

    while(--argc>0){
        printf("%s%s \n", *++argv, (argc>1)? " ":"");
    }
    printf("\n");

    return 0;
}

int binSearch( int x, int v[], int n){
    int low, high, mid;

    low = 0;
    high = n-1;

    while(low <= high){
        mid = (low+high)/2;
        if(x < v[mid])
            high = mid+1;
        else if(x > v[mid])
            low = mid + 1;
        else
            return mid;
    }
    return -1;

}


int twoSum(int numbers[], int n, int target) {
    int index1, index2, j, i;
    int found = 0;
    for(i = 0; i<n-1; i++){
        for(j = i+1; j<=n-1; j++){
            printf("i is %d, j is %d, index1 is %d \n", i, j, index1);
            if((numbers[i] + numbers[j]) == target){
                index1 = i; index2 = j; found = 1;
                break;
            }
        }
        if(found > 0)
            break;
    }
    printf("index1 = %d, index2 = %d \n", ++index1, ++index2);
    return 0;

}

void reverse(char s[]){
    int c, i, j;

    for(i=0, j=strlen(s)-1; i<j ; i++, j--){
        c = s[i];
        s[i] = s[j];
        s[j] = c;
    }
}

/*int strLen(char *s){
    int n;
    for ( n = 0; (*s) != "\0"; s++)
    {
        n++;
    }
    return n;
}
*/

