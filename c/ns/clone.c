#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <sched.h>
#include <signal.h>
#include <unistd.h>
 
/* 定义一个给 clone 用的栈，栈大小1M */
#define STACK_SIZE (1024 * 1024)
static char container_stack[STACK_SIZE];
 
char* const container_args[] = {
    "/bin/bash",
    NULL
};
 
int container_main(void* arg)
{
    printf("Container - inside the container!\n");
    /* 直接执行一个shell，以便我们观察这个进程空间里的资源是否被隔离了 */

    printf("Container [%5d] - inside the container!\n", getpid());

    sethostname("container",10); /* 设置hostname */

    /* 重新mount proc文件系统到 /proc下 */
    system("mount -t proc proc /proc");

    execv(container_args[0], container_args); 
    printf("Something's wrong!\n");
    return 1;
}
 
int main()
{
    printf("Parent [%5d] - start a container!\n", getpid());

    /* 调用clone函数，其中传出一个函数，还有一个栈空间的（为什么传尾指针，因为栈是反着的） */
    int container_pid = clone(container_main, container_stack+STACK_SIZE, 
        CLONE_NEWNS | CLONE_NEWPID | CLONE_NEWIPC | CLONE_NEWUTS | SIGCHLD, NULL);
    /* 等待子进程结束 */
    waitpid(container_pid, NULL, 0);
    printf("Parent - container stopped! container_pid is %d \n", container_pid);
    return 0;
}