#!/usr/bin/env python3
"""Literal permutation enumeration of DEFINITION.md (independent check, n = 3..6).

Enumerates every ordering p_1..p_{2n} of the eyelets 1..2n with p_1 = 1 and
p_{2n} = 2n (rule 1 fixes those two, so only the 2n-2 middle eyelets are
permuted), and tests rules 2 and 3 literally on the whole sequence.
Also checks the mirror-image claim (mirror is a lacing, never equal).
Usage: python3 brute_check.py [nmax]   (default nmax = 6; n = 6 takes ~1 min)
"""
import sys
from itertools import permutations


def is_lacing(p, n):
    N = 2 * n
    if len(p) != N or sorted(p) != list(range(1, N + 1)):
        return False
    if p[0] != 1 or p[-1] != N:                       # rule 1
        return False
    for i in range(N - 1):                             # rule 2
        if p[i] + p[i + 1] == N + 1:
            return False
    for i in range(N - 2):                             # rule 3
        t = p[i:i + 3]
        if all(e <= n for e in t) or all(e > n for e in t):
            return False
    return True


def brute_D(n):
    N = 2 * n
    count = 0
    for mid in permutations(range(2, N)):
        p = (1,) + mid + (N,)
        if is_lacing(p, n):
            count += 1
            q = tuple(N + 1 - e for e in reversed(p))   # mirror image
            assert is_lacing(q, n) and q != p
    return count


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    for n in range(3, nmax + 1):
        D = brute_D(n)
        assert D % 2 == 0
        print(n, D, D // 2, flush=True)
