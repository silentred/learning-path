#include <unistd.h>
#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/wait.h>

int main() {
    pid_t pid;
    int fd;
    int num = 917;

    // create shared mem
    fd = shm_open("/test", O_CREAT | O_RDWR, 0666);
    ftruncate(fd, sizeof(int));
    write(fd, &num, sizeof(int));
    printf("fd=%d \n", fd);

    pid = fork();    
    if (pid > 0) {
        // parent
        printf("parent \n");
        if (waitpid(pid, NULL, 0) != pid) {
            printf("waitpid error\n");
        }
    } else if (pid == 0) {
        // child
        //execv("./echo", NULL);
        int newNum;
        ssize_t readsize;
        fd = shm_open("/test",  O_RDWR, 0666);
        readsize = read(fd, &newNum, sizeof(int));
        printf("child, fd=%d, num=%d \n", fd, newNum);
        sleep(1);
    } else {
        printf("fork error \n");
    }
}