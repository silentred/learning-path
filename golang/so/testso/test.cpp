#include "libtestso.h"
#include <iostream>

int main() {
    std::cout << "This is a Cpp Application." << std::endl;
  
    GoString name = {"Jack", 4};
    SayHello(name);
    SayBye();

    return 0;
}