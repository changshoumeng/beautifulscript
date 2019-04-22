import math
import sys


def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def subcompute(x, a, m):
    print("subcompute:", x, a, m)
    b = m
    count = 0
    while b < x - 1:
        if not isPrime(b):
            b += 1
            continue
        count += 1
        c =  a * b
        if c == x:
            #('result:', 63, 83777, 85229)
            print("result:", count, a, b)
            sys.exit(1)
        if count > 1000000:
            print("run too many times,not get result")
            sys.exit(1)
        if c > x:
            return
        b += 1
        #print(count)


def compute(x):
    m = int(x**0.5)
    a = m
    while a > 2:
        if not isPrime(a):
            a -= 1
            continue
        subcompute(x, a, m)
        a -= 1

def main():
    compute(7140229933)


if __name__ == '__main__':
    main()
