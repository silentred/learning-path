#include <unistd.h>
#include <stdio.h>

int main() {
    pid_t pid;

    pid = fork();
    
    if (pid > 0) {
        // parent
        printf("parent \n");
    } else if (pid == 0) {
        // child
        execv("./echo", NULL);
        sleep(1);
    } else {
        printf("for error \n");
    }
}