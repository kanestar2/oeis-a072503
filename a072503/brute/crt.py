#!/usr/bin/env python3
"""Combine D mod 2^64 and D mod (2^61-1) (outputs of subset_dp MODE=1 / MODE=2)
into the exact D by the Chinese remainder theorem (valid while D < 2^125).

Usage: python3 crt.py <D mod 2^64> <D mod 2^61-1>
"""
import sys

m1, m2 = 2**64, 2**61 - 1
r1, r2 = int(sys.argv[1]), int(sys.argv[2])
# x = r1 + m1*t,  x = r2 (mod m2)
t = ((r2 - r1) * pow(m1, -1, m2)) % m2
D = r1 + m1 * t
assert D % m1 == r1 and D % m2 == r2
assert D < 2**125, "too large for this CRT"
assert D % 2 == 0, "D must be even"
print(f"D={D} a={D // 2}")
