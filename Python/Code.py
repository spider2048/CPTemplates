import os
import sys
import time
import heapq
import itertools
import functools
import time
from collections import *

MULTIPLE_TESTS = False


def inp(ty=int):
    return list(map(ty, input().split(" ")))


def solve():
    print("3 + 3 =", 6)


def main():
    if MULTIPLE_TESTS:
        for _ in range(int(input())):
            solve()
    else:
        solve()


if __name__ == "__main__":
    if os.environ.get("LOCAL"):
        from local import ProcessHandler

        ProcessHandler(
            main=main,
            props={"input": "input.txt", "code": __file__},
            monitor=["Code.py", "input.txt"],
            timeout=1,
        )
    else:
        main()
