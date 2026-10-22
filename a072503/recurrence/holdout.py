#!/usr/bin/env python3
"""Holdout test of the guessed recurrence (order R, degree d) for T(n) = D(n)/(n-1)!:
fit the coefficients modulo prime p using only n <= NFIT, then check the
recurrence on all remaining n.  Usage: python3 holdout.py R d NFIT p"""
import sys, numpy as np
from math import factorial
R, d, NFIT, p = map(int, sys.argv[1:5])
u = {}
for l in open('../method_ie/results.txt'):
    n, D, a = map(int, l.split()); u[n] = D // factorial(n - 1)
N0, N1 = min(u), max(u)
def row(n): return [pow(n, j, p) * (u[n + i] % p) % p for i in range(R + 1) for j in range(d + 1)]
M = np.array([row(n) for n in range(N0, NFIT - R + 1)], dtype=object)
# nullspace mod p by Gaussian elimination (object dtype: exact python ints)
M = [list(r) for r in M]; cols = (R + 1) * (d + 1); piv = []; r = 0
for c in range(cols):
    k = next((i for i in range(r, len(M)) if M[i][c] % p), None)
    if k is None: continue
    M[r], M[k] = M[k], M[r]; inv = pow(M[r][c], p - 2, p); M[r] = [x * inv % p for x in M[r]]
    for i in range(len(M)):
        if i != r and M[i][c] % p:
            f = M[i][c]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
    piv.append(c); r += 1
free = [c for c in range(cols) if c not in piv]
print(f"p = {p}: order {R} degree {d}, fit n<= {NFIT}: equations {NFIT-R-N0+1}, unknowns {cols}, nullity {len(free)}")
if len(free) == 1:
    v = [0] * cols; v[free[0]] = 1
    for i, c in enumerate(piv): v[c] = (-M[i][free[0]]) % p
    bad = [n for n in range(NFIT - R + 1, N1 - R + 1) if sum(x * y for x, y in zip(v, row(n))) % p]
    print(f"checked on n = {NFIT-R+1}..{N1-R} (terms up to a({N1})): failures {bad[:10]} ({len(bad)})")
