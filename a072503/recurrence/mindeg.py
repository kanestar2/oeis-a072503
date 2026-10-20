#!/usr/bin/env python3
"""Minimal degree d of a recurrence of order R for u = T(n) = D(n)/(n-1)!, mod p.
Usage: python3 mindeg.py R1 R2 [terms_file]"""
import sys, numpy as np
from math import factorial
sys.argv += [] 
import importlib.util
p = 2147483629
R1, R2 = int(sys.argv[1]), int(sys.argv[2])
src = sys.argv[3] if len(sys.argv) > 3 else '../method_ie/results.txt'
u = {}
for l in open(src):
    n, D, a = map(int, l.split()); u[n] = D // factorial(n - 1)
ns = sorted(u); N0, N1 = ns[0], ns[-1]
def rank_mod(M):
    M = M.copy() % p; rows, cols = M.shape; r = 0
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        piv = r + nz[0]; M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
        f = M[:, c].copy(); f[r] = 0; nzr = np.nonzero(f)[0]
        if len(nzr): M[nzr] = (M[nzr] - (f[nzr, None] * M[r][None, :]) % p) % p
        r += 1
        if r == rows: break
    return r
def nullity(R, d):
    neq = N1 - R - N0 + 1; cols = (R + 1) * (d + 1)
    M = np.zeros((neq, cols), dtype=np.int64)
    for row, n in enumerate(range(N0, N1 - R + 1)):
        for i in range(R + 1):
            ui = u[n + i] % p
            for j in range(d + 1): M[row, i * (d + 1) + j] = pow(n, j, p) * ui % p
    return cols - rank_mod(M), cols, neq
for R in range(R1, R2 + 1):
    lo = 0
    for d in range(0, 60):
        k, cols, neq = nullity(R, d)
        if neq - cols < 30: print(f"order {R}: none up to degree {d-1}"); break
        if k > 0: print(f"order {R}: minimal degree {d} (nullity {k}, unknowns {cols}, eqs {neq})", flush=True); break
