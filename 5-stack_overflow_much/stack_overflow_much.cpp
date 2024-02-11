#include <iostream>
#include <sys/resource.h>

int endlessRecursion(int x) {
  std::cout << "depth: " << x << std::endl;
  float big_array[100000];
  endlessRecursion(x+1);
}

int main() { 
    struct rlimit stack_rlimit;
    if (getrlimit(RLIMIT_STACK, &stack_rlimit) == 0) {
        std::cout << "Stack (soft, hard) = (" << stack_rlimit.rlim_cur << ", " << stack_rlimit.rlim_max << ")\n";
    } 

    endlessRecursion(0);
    
}