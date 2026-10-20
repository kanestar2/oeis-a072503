#!/usr/bin/env python3
"""For each order R, test whether u(n) satisfies ANY recurrence
   sum_{i=0..R} P_i(n) u(n+i) = 0 with deg P_i <= d_max(R), where d_max(R) is the
largest degree that the available terms can still test with >= 30 spare equations.
Rank computed modulo a 31-bit prime with numpy.  Nullity 0 => no such recurrence.
Usage: python3 guess_np.py [a|T|D] RMAX [terms_file]
"""
import sys, numpy as np
from math import factorial
p = 2147483629
which, RMAX = sys.argv[1], int(sys.argv[2])
src = sys.argv[3] if len(sys.argv) > 3 else '../accepted_terms.txt'
a = {}
for l in open(src):
    n, v, *rest = map(int, l.split())
    a[n] = v if not rest else rest[0]
u = {n: (2 * v // factorial(n - 1)) if which == 'T' else (2 * v if which == 'D' else v) for n, v in a.items()}
ns = sorted(u); N0, N1 = ns[0], ns[-1]

def rank_mod(M):
    M = M.copy() % p; rows, cols = M.shape; r = 0
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        piv = r + nz[0]
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        f = M[:, c].copy(); f[r] = 0
        nzr = np.nonzero(f)[0]
        if len(nzr):
            M[nzr] = (M[nzr] - (f[nzr, None] * M[r][None, :]) % p) % p
        r += 1
        if r == rows: break
    return r

for R in range(1, RMAX + 1):
    neq = N1 - R - N0 + 1
    d = (neq - 30) // (R + 1) - 1
    if d < 0: break
    cols = (R + 1) * (d + 1)
    M = np.zeros((neq, cols), dtype=np.int64)
    for row, n in enumerate(range(N0, N1 - R + 1)):
        for i in range(R + 1):
            ui = u[n + i] % p
            for j in range(d + 1):
                M[row, i * (d + 1) + j] = pow(n, j, p) * ui % p
    k = cols - rank_mod(M)
    print(f"{which}: order {R:2d}, degree <= {d:3d}: unknowns {cols}, equations {neq}, nullity {k}", flush=True)
