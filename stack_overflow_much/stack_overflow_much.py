import sys
import resource

def endless_recursion(depth=0):
    mem = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024/1024, 3)
    big_list = list(range(10**5))
    print(f"depth={depth} memory_gb={mem}")
    endless_recursion(depth+1)

def main():
    stack = resource.getrlimit(resource.RLIMIT_STACK)
    print(f"Stack (soft, hard) =  {stack}")
    sys.setrecursionlimit(10**7)
    endless_recursion(0)

if __name__ == "__main__":
    main()