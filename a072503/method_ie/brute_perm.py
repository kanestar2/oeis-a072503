#!/usr/bin/env python3
"""Literal brute force straight from DEFINITION.md (independent of the formula).

Enumerates every ordering p_1..p_{2n} of the eyelets 1..2n with p_1 = 1 and
p_{2n} = 2n (itertools.permutations of the 2n-2 middle eyelets) and checks
rules 2 and 3 literally.  Prints D(n), a(n) and the count per side word
(the word over {L,R} giving the side of p_1..p_{2n}).

usage: python3 brute_perm.py N_MIN N_MAX      (n = 6 takes ~10 s)
"""
import sys
from itertools import permutations
from collections import Counter


def is_lacing(p, n):
    m = 2 * n
    if p[0] != 1 or p[-1] != m:                      # rule 1
        return False
    if sorted(p) != list(range(1, m + 1)):          # every eyelet once
        return False
    for i in range(m - 1):                          # rule 2
        if p[i] + p[i + 1] == m + 1:
            return False
    for i in range(m - 2):                          # rule 3
        a, b, c = p[i], p[i + 1], p[i + 2]
        if (a <= n and b <= n and c <= n) or (a > n and b > n and c > n):
            return False
    return True


def brute(n):
    m = 2 * n
    middle = list(range(2, m))
    per_word = Counter()
    total = 0
    for mid in permutations(middle):
        p = (1,) + mid + (m,)
        if is_lacing(p, n):
            total += 1
            per_word[''.join('L' if e <= n else 'R' for e in p)] += 1
    return total, per_word


if __name__ == '__main__':
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for n in range(lo, hi + 1):
        D, pw = brute(n)
        print(f"n={n} D={D} a={D // 2} even={D % 2 == 0}")
        for w in sorted(pw):
            print(f"  {w} {pw[w]}")
