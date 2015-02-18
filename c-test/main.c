#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    int len;
    len = strlen("ccc");
    printf("Hello world!\n");
    printf("string length is %d", len);

    int heap[6] = {1,2,3,4,5,6};
    int x = 3;
    int result;
    //result = binSearch(x, heap, sizeof(heap));
    //printf("Index is %d", result);

    int num[4] = {2, 7, 11, 15};
    len = sizeof(num)/sizeof(int);
    twoSum(num, len, 9);

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
    printf("index1 = %d, index2 = %d", ++index1, ++index2);
    return 0;

}
