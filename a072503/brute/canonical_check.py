#!/usr/bin/env python3
"""Check by literal enumeration (n = 3..6) that D(n)/(n-1)! equals the number of
lacings in which the inner rows 2..n are first visited in increasing order.
Usage: python3 canonical_check.py NMAX"""
import sys
from itertools import permutations
from math import factorial
for n in range(3, int(sys.argv[1]) + 1):
    N = 2 * n; tot = canon = 0
    for mid in permutations(range(2, N)):
        p = (1,) + mid + (N,)
        if any(p[i] + p[i + 1] == N + 1 for i in range(N - 1)): continue
        s = [x <= n for x in p]
        if any(s[i] == s[i + 1] == s[i + 2] for i in range(N - 2)): continue
        tot += 1
        rows = [min(x, N + 1 - x) for x in p[1:-1]]
        first = [r for i, r in enumerate(rows) if r not in rows[:i]]
        canon += first == sorted(first)
    print(f"n={n}: D={tot}, D/(n-1)!={tot // factorial(n - 1)} (exact: {tot % factorial(n - 1) == 0}), canonical lacings={canon}")
