#!/usr/bin/env python3
"""Reviewer's own implementation of the explicit sum stated in method_ie/METHOD.md §5,
written from the text of METHOD.md (formula.py not used):

  a(n) = (n-1)!/2 * sum_{r,q,Z,e,a,c} (-1)^(r-1-Z+e) C(Z-1,q-1) C(r-Z,q) C(q,a) C(q,c)
            C(r-q-Z,e) C(r-q-e, n-r-a-e) C(r-q-e, n-r-c-e) Delta(n-r+Z-e, Z-q+a+c),
  Delta(M,b) = sum_j (-1)^j C(b,j) (M-j)!,
  1 <= r <= n, 0 <= q <= Z <= r-1, q+Z <= r, 0 <= e <= r-q-Z, 0 <= a,c <= q,
  convention C(-1,-1) = 1.

Delta is tabulated by the recurrence Delta(M,b) = Delta(M,b-1) - Delta(M-1,b-1).
Compares with accepted_terms.txt.   Usage: python3 closed_form.py NMAX
"""
import sys
import time
from math import comb, factorial


def C(x, y):
    if x == -1 and y == -1:
        return 1
    if x < 0 or y < 0 or y > x:
        return 0
    return comb(x, y)


def make_delta(MM):
    D = {}
    for M in range(0, MM + 1):
        D[(M, 0)] = factorial(M)
    for b in range(1, MM + 1):
        for M in range(b, MM + 1):
            D[(M, b)] = D[(M, b - 1)] - D[(M - 1, b - 1)]
    return D


def a_closed(n, DL):
    tot = 0
    for r in range(1, n + 1):
        for Z in range(0, r):
            for q in range(0, Z + 1):
                if q + Z > r:
                    continue
                w1 = C(Z - 1, q - 1) * C(r - Z, q)
                if not w1:
                    continue
                for e in range(0, r - q - Z + 1):
                    w2 = w1 * C(r - q - Z, e)
                    M = r - q - e
                    sg = -1 if (r - 1 - Z + e) % 2 else 1
                    for a in range(0, q + 1):
                        wa = w2 * C(q, a) * C(M, n - r - a - e)
                        if not wa:
                            continue
                        for c in range(0, q + 1):
                            wc = wa * C(q, c) * C(M, n - r - c - e)
                            if not wc:
                                continue
                            Mx, b = n - r + Z - e, Z - q + a + c
                            assert 0 <= b <= Mx, (n, r, q, Z, e, a, c)
                            tot += sg * wc * DL[(Mx, b)]
    D = factorial(n - 1) * tot
    assert D % 2 == 0
    return D // 2


if __name__ == "__main__":
    NMAX = int(sys.argv[1])
    acc = {}
    for line in open(__file__.rsplit("/", 2)[0] + "/accepted_terms.txt"):
        k, v = map(int, line.split())
        acc[k] = v
    DL = make_delta(2 * NMAX + 2)
    t0 = time.time()
    ok = True
    for n in range(3, NMAX + 1):
        v = a_closed(n, DL)
        same = v == acc[n]
        ok &= same
        print(f"n={n} closed-form == accepted: {same}  ({time.time() - t0:.1f}s)", flush=True)
    print("ALL OK" if ok else "FAILED")
