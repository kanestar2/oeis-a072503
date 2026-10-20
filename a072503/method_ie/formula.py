#!/usr/bin/env python3
"""Explicit finite binomial sum for N_n(k) and a(n) (see METHOD.md, section 5),
plus a cross-check against the DP (ie_dp.py) and the word enumeration
(ie_per_word.py).

  N_n(k) = sum_{r,q,Z,e,x,y} C(Z-1,q-1) C(r-Z,q) C(q,x) C(q,y) C(r-q-Z,e)
             * C(r-q-e, n-r-x-e) C(r-q-e, n-r-y-e) C(Z-q+x+y, k-r+1+Z-e)

  D(n) = (n-1)! sum_{r,q,Z,e,x,y} (-1)^(r-1-Z+e) C(Z-1,q-1) C(r-Z,q) C(q,x) C(q,y)
             * C(r-q-Z,e) C(r-q-e, n-r-x-e) C(r-q-e, n-r-y-e) Delta(n-r+Z-e, Z-q+x+y)

  Delta(M, b) = sum_j (-1)^j C(b,j) (M-j)!  (permutations of M points with no
  fixed point among b given points).

usage: python3 formula.py NMAX_CHECK
"""
import sys
from math import comb, factorial


def C(a, b):
    if a == -1 and b == -1:
        return 1            # the q = Z = 0 term (no zero block)
    if a < 0 or b < 0 or b > a:
        return 0
    return comb(a, b)


def N_formula(n):
    res = [0] * (2 * n + 2)
    for r in range(1, n + 1):
        for q in range(0, r + 1):
            for Z in range(0, r):
                w1 = C(Z - 1, q - 1) * C(r - Z, q)
                if not w1 or r - q - Z < 0:
                    continue
                for e in range(0, r - q - Z + 1):
                    w2 = w1 * C(r - q - Z, e)
                    M = r - q - e
                    for x in range(0, q + 1):
                        wx = w2 * C(q, x) * C(M, n - r - x - e)
                        if not wx:
                            continue
                        for y in range(0, q + 1):
                            wy = wx * C(q, y) * C(M, n - r - y - e)
                            if not wy:
                                continue
                            beta = Z - q + x + y
                            for j in range(0, beta + 1):
                                k = r - 1 - Z + e + j
                                res[k] += wy * C(beta, j)
    while res and res[-1] == 0:
        res.pop()
    return res


def Delta(M, b):
    return sum((-1) ** j * comb(b, j) * factorial(M - j) for j in range(b + 1))


def D_formula(n):
    tot = 0
    for r in range(1, n + 1):
        for q in range(0, r + 1):
            for Z in range(0, r):
                w1 = C(Z - 1, q - 1) * C(r - Z, q)
                if not w1 or r - q - Z < 0:
                    continue
                for e in range(0, r - q - Z + 1):
                    w2 = w1 * C(r - q - Z, e)
                    M = r - q - e
                    for x in range(0, q + 1):
                        wx = w2 * C(q, x) * C(M, n - r - x - e)
                        if not wx:
                            continue
                        for y in range(0, q + 1):
                            wy = wx * C(q, y) * C(M, n - r - y - e)
                            if wy:
                                tot += (-1) ** (r - 1 - Z + e) * wy * Delta(n - r + Z - e, Z - q + x + y)
    return factorial(n - 1) * tot


if __name__ == '__main__':
    sys.path.insert(0, __import__('os').path.dirname(__file__))
    import ie_dp
    import ie_per_word
    NM = int(sys.argv[1])
    sv = ie_dp.Solver(ie_dp.coef_bits(NM))
    sv.init()
    ok = True
    for n in range(1, NM + 1):
        sv.compute_layer(n)
        if n < 2:
            continue
        Nd = sv.N_of(n)
        Nf = N_formula(n)
        same = (Nd == Nf)
        line = f"n={n}: DP N_n(k) == explicit formula: {same}"
        if n <= 11:
            tot = [0] * n
            for w in ie_per_word.words(n):
                for k, c in enumerate(ie_per_word.mk(w, n)):
                    tot[k] += c
            while tot and tot[-1] == 0:
                tot.pop()
            line += f"; == word enumeration: {tot == Nd}"
            same &= (tot == Nd)
        Dd = ie_dp.D_from_N(n, Nd)
        Df = D_formula(n)
        line += f"; D via Delta-sum equal: {Dd == Df}; a={Dd // 2}"
        same &= (Dd == Df)
        ok &= same
        print(line, flush=True)
    print("ALL OK" if ok else "FAILED")
