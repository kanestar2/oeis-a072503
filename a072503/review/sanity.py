#!/usr/bin/env python3
"""Reviewer's sanity checks on the result files (read only).

1. accepted_terms.txt is exactly {n: a(n)} for the n common to both results
   files, both files agree there, and the format is a clean b-file.
2. Divisibility: D(n) = 2 a(n) must be divisible by (n-1)! (row relabelling acts
   freely); report the parity of C(n) = D(n)/(n-1)! (= a(n) divisible by (n-1)!?)
   and C(n) against the canonical enumeration (review/canon_enum, n <= 11).
3. Growth: rho(n) = D(n) / ((n-1)!^2 W(n)), W(n) = number of admissible side
   words, should converge smoothly (it is the probability that a uniformly random
   (sigma, tau) for a random word avoids all horizontals, ~ e^{-c});
   and a(n+1)/a(n) / n^2 should converge to the side-word growth rate.
4. Digit lengths (OEIS b-file and DATA-section limits).
"""
import math
from fractions import Fraction

ROOT = __file__.rsplit("/", 2)[0]


def load3(p):
    d, raw = {}, open(p).read()
    assert raw.endswith("\n")
    for line in raw.splitlines():
        n, D, a = line.split()
        assert str(int(n)) == n and str(int(D)) == D and str(int(a)) == a
        n, D, a = int(n), int(D), int(a)
        assert n not in d and D == 2 * a
        d[n] = a
    return d


dp = load3(ROOT + "/method_dp/results.txt")
ie = load3(ROOT + "/method_ie/results.txt")
raw = open(ROOT + "/accepted_terms.txt").read()
acc_lines = raw.splitlines()
acc = {}
for line in acc_lines:
    parts = line.split(" ")
    assert len(parts) == 2 and parts[0] == str(int(parts[0])) and parts[1] == str(int(parts[1])), line
    acc[int(parts[0])] = int(parts[1])
common = sorted(set(dp) & set(ie))
print("1. dp range", min(dp), max(dp), "ie range", min(ie), max(ie))
print("   accepted == common part:", sorted(acc) == common and all(acc[n] == dp[n] == ie[n] for n in common),
      "| n ascending contiguous:", [int(l.split()[0]) for l in acc_lines] == list(range(3, max(common) + 1)),
      "| ends with newline:", raw.endswith("\n"), "| no CR/tabs:", "\r" not in raw and "\t" not in raw)
print("   ie-only terms n =", min(set(ie) - set(dp)), "..", max(set(ie) - set(dp)), "(not accepted, not cross-checked by method_dp)")

# 2. divisibility
canon = {3: 3, 4: 15, 5: 152, 6: 1826, 7: 26446, 8: 454388, 9: 8982734, 10: 200843362, 11: 5015991284}
bad = [n for n in common if (2 * acc[n]) % math.factorial(n - 1)]
Cn = {n: 2 * acc[n] // math.factorial(n - 1) for n in common}
print("2. D(n) divisible by (n-1)! for all n:", not bad)
print("   C(n) = D(n)/(n-1)! equals canonical enumeration (n=3..11):", all(Cn[n] == canon[n] for n in canon))
odd = [n for n in common if Cn[n] % 2]
print("   n with C(n) odd (a(n) NOT divisible by (n-1)!):", odd[:20], "... count", len(odd))
# extra power of small primes beyond (n-1)!
def v(p, x):
    k = 0
    while x % p == 0:
        x //= p; k += 1
    return k
print("   v2(C(n)) n=3..30:", [v(2, Cn[n]) for n in range(3, 31)])
print("   gcd(C(n), (n-1)!) n=3..20:", [math.gcd(Cn[n], math.factorial(n - 1)) for n in range(3, 21)])

# 3. growth
def words(n):
    # admissible side words: w1=L, w2n=R, n L's and n R's, runs of length 1 or 2
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def f(i, h, s, r):
        if i == n and h == n:
            return 1 if s == 1 else 0
        tot = 0
        for x in (0, 1):
            if x == s and r == 2:
                continue
            i2, h2 = i + (x == 0), h + (x == 1)
            if i2 > n or h2 > n:
                continue
            tot += f(i2, h2, x, r + 1 if x == s else 1)
        return tot
    return f(1, 0, 0, 1)
print("3. rho(n) = D(n)/((n-1)!^2 W(n)) and r(n) = a(n+1)/(a(n) n^2):")
prev = None
for n in [3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 75, 100, 150, 200, 250, 300, 350, 399, 400]:
    W = words(n)
    rho = Fraction(2 * acc[n], math.factorial(n - 1) ** 2 * W)
    rr = Fraction(acc[n + 1], acc[n] * n * n) if n + 1 in acc else None
    print(f"   n={n:4d} W(n)={W if n < 20 else '%.4e' % W}  rho={float(rho):.10f}  "
          f"r(n)={'%.8f' % float(rr) if rr else '-'}  rho*W/W'..")
# smoothness: second differences of log a(n) - 2 log (n-1)!
vals = {n: math.log(acc[n]) - 2 * math.lgamma(n) for n in common}
d2 = [vals[n + 1] - 2 * vals[n] + vals[n - 1] for n in common[1:-1]]
print("   2nd differences of log(a(n)/(n-1)!^2): min %.3e max %.3e, sign changes %d (n>=10)" % (
    min(d2[7:]), max(d2[7:]), sum(1 for x, y in zip(d2[7:], d2[8:]) if (x > 0) != (y > 0))))
rhos = [Fraction(2 * acc[n], math.factorial(n - 1) ** 2 * words(n)) for n in range(3, 401)]
diffs = [float(rhos[i + 1] - rhos[i]) for i in range(len(rhos) - 1)]
# diffs[i] = rho(i+4) - rho(i+3), so diffs[N0-3:] covers rho(N0), ..., rho(400).
# (Edited 2026-10-22: the message used to say "from n=3" while diffs[5:], i.e. n >= 8,
# was tested; rho rises from n = 4 to n = 5.)
N0 = 5
print("   rho(n) monotone for n = %d..400:" % N0,
      "increasing" if all(x > 0 for x in diffs[N0 - 3:]) else ("decreasing" if all(x < 0 for x in diffs[N0 - 3:]) else "NOT monotone"),
      "| first diffs n=3..12:", ["%.2e" % x for x in diffs[:10]])
print("   limit guess e^{-4/3}*?: rho(400) = %.8f, e^{-4/3} = %.8f" % (float(rhos[-1]), math.exp(-4 / 3)))

# 4. digits
dig = {n: len(str(acc[n])) for n in common}
last1000 = max(n for n in common if dig[n] <= 1000)
print(f"4. digits: a(400) has {dig[400]} digits; largest n with <= 1000 digits: {last1000} ({dig[last1000]} digits)")
s = ""
for n in common:
    t = (", " if s else "") + str(acc[n])
    if len(s) + len(t) > 260:
        break
    s += t
print(f"   DATA section (<= 260 chars) would hold a(3..{n - 1})")
