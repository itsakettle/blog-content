import sys
import resource

def endless_recursion(depth=0):
    memory_gb = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024/1024, 3)
    big_list = list(range(10**5))
    print(f"depth={depth} memory_gb={memory_gb}")
    endless_recursion(depth+1)

def main():
    stack_size = resource.getrlimit(resource.RLIMIT_STACK)
    print(f"Stack (soft, hard) =  {stack_size}")
    sys.setrecursionlimit(10**7)
    endless_recursion(0)

if __name__ == "__main__":
    main()