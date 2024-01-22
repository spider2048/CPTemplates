import os
import sys
import time
import heapq
import itertools
import functools
import time

MULTIPLE_TESTS = False


def inp():
    return list(map(int, input().split(" ")))


def solve():
    print(1 + 1)


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
