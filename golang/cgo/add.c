// 引用 GO 中的函数
extern void myprint(int i);

int add(int a) {
    myprint(a+2);
    return a+1;
}