#!/usr/bin/env python3
"""Search for a linear recurrence with polynomial coefficients
   sum_{i=0..R} P_i(n) * u(n+i) = 0,  deg P_i <= d,
satisfied by u(n) = a(n) (or by D(n)/(n-1)!), working modulo a large prime.
Reports the (R, d) pairs where the solution space is non-trivial.
Usage: python3 guess_mod.py [a|T] RMAX DMAX
"""
import sys
from math import factorial
p = (1 << 61) - 1
which, RMAX, DMAX = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
a = {}
for l in open('../accepted_terms.txt'):
    n, v = map(int, l.split()); a[n] = v
if which == 'T':
    u = {n: (2 * v // factorial(n - 1)) for n, v in a.items()}
else:
    u = a
ns = sorted(u)

def nullity(R, d):
    cols = (R + 1) * (d + 1)
    rows = []
    for n in ns:
        if n + R > ns[-1]: break
        rows.append([pow(n, j, p) * (u[n + i] % p) % p for i in range(R + 1) for j in range(d + 1)])
        if len(rows) >= cols + 20: break
    if len(rows) < cols + 5: return None
    # rank mod p
    M = rows; rank = 0; c = 0
    for c in range(cols):
        piv = next((r for r in range(rank, len(M)) if M[r][c]), None)
        if piv is None: continue
        M[rank], M[piv] = M[piv], M[rank]
        inv = pow(M[rank][c], p - 2, p)
        M[rank] = [x * inv % p for x in M[rank]]
        for r in range(len(M)):
            if r != rank and M[r][c]:
                f = M[r][c]
                M[r] = [(x - f * y) % p for x, y in zip(M[r], M[rank])]
        rank += 1
    return cols - rank

for R in range(1, RMAX + 1):
    for d in range(0, DMAX + 1):
        k = nullity(R, d)
        if k is None: break
        if k > 0:
            print(f"{which}: order {R}, degree {d}: nullity {k}", flush=True)
            break
    else:
        print(f"{which}: order {R}: nothing up to degree {DMAX}", flush=True)
