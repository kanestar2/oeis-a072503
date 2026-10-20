#!/usr/bin/env python3
"""rho(n) = D(n) / A078698(n) = D(n) / ((n-1)!^2 * A051286(n)) is the fraction of
lacings of A078698 (same rules, no horizontal ban) that avoid all horizontals.
Poisson heuristic: a uniformly random admissible word has ~2n/mu switch places,
mu = mean run length = 1/phi + 2/phi^2, and each is horizontal with probability
1/(n-1); so rho(n) -> exp(-2/mu) = exp(-(1 + 1/sqrt(5))).
Richardson extrapolation of the accepted terms (read only)."""
from math import comb, factorial, exp, sqrt
from fractions import Fraction
acc = {}
for line in open(__file__.rsplit('/', 2)[0] + '/accepted_terms.txt'):
    n, a = map(int, line.split()); acc[n] = a
W = lambda n: sum(comb(n - k, k) ** 2 for k in range(n // 2 + 1))
rho = lambda n: Fraction(2 * acc[n], factorial(n - 1) ** 2 * W(n))
r = {n: float(rho(n)) for n in (50, 100, 200, 400)}
R1 = {n: 2 * r[2 * n] - r[n] for n in (50, 100, 200)}          # kills 1/n
R2 = {n: (4 * R1[2 * n] - R1[n]) / 3 for n in (50, 100)}       # kills 1/n^2
phi = (1 + sqrt(5)) / 2
print("rho(n):", {n: round(v, 10) for n, v in r.items()})
print("Richardson 1:", {n: round(v, 10) for n, v in R1.items()})
print("Richardson 2:", {n: round(v, 10) for n, v in R2.items()})
print("2/mu =", 2 / (1 / phi + 2 / phi ** 2), " 1+1/sqrt5 =", 1 + 1 / sqrt(5))
print("exp(-(1+1/sqrt5)) =", round(exp(-(1 + 1 / sqrt(5))), 10))
