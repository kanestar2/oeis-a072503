#!/usr/bin/env python3
"""Combine D(n) mod 2^64 and D(n) mod (2^61-1) (outputs of subset_dp MODE=1 / MODE=2)
into the exact D(n) by the Chinese remainder theorem.

Why this is exact: D(n) counts orderings of the 2n-2 inner eyelets, so
0 <= D(n) <= (2n-2)!.  The CRT gives the unique value in [0, 2^64*(2^61-1));
it is D(n) itself whenever (2n-2)! < 2^64*(2^61-1), i.e. for n <= 17 (32! < 2^125);
here it is used for n = 12, 13
(for n = 13: D(13) <= 24! < 2^80).  The script refuses larger n.

Usage: python3 crt.py n <D mod 2^64> <D mod 2^61-1>
"""
import sys
from math import factorial

n = int(sys.argv[1])
m1, m2 = 2**64, 2**61 - 1
r1, r2 = int(sys.argv[2]), int(sys.argv[3])
assert factorial(2 * n - 2) < m1 * m2, "n too large: (2n-2)! does not fit below 2^64*(2^61-1)"
# x = r1 + m1*t,  x = r2 (mod m2)
t = ((r2 - r1) * pow(m1, -1, m2)) % m2
D = r1 + m1 * t
assert D % m1 == r1 and D % m2 == r2
assert D <= factorial(2 * n - 2)
assert D % 2 == 0, "D must be even"
print(f"D={D} a={D // 2}")
