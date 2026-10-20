#!/usr/bin/env python3
"""Cross-check of the model against Pfoertner's sister sequences (own code).

A078698(n): directed lacings, begin/end at the extreme pair, "each eyelet has at
  least one direct connection to the opposite side"; proven closed form
  (n-1)!^2 * A051286(n), A051286(n) = sum_k C(n-k,k)^2.
A078702(n) = (A078698(n) + A078700(n))/2: the same lacings up to reversal+mirror,
  A078700 = number of symmetric ones.
Checks:
 1. reading C WITHOUT the horizontal ban (literal enumeration, n = 3..6)
    = A078698(n), and the number of lacings fixed by the mirror map
    mu(p)_i = 2n+1 - p_{2n+1-i} (DEFINITION.md) = 2*A078702(n) - A078698(n);
    with the ban, the number of mu-fixed lacings is 0 (n = 3..6).
 2. a COPY of method_dp/short.py's transition, with the rule-2 correction removed
    (one line), reproduces (n-1)!^2 * A051286(n) for n = 3..60 and the A078698
    data to n = 17 (tests the profile machinery independently of rule 2).
 3. The k = 0 term of the IE formula, (n-1)!^2 * W(n), is A078698(n).
"""
from functools import lru_cache
from math import comb, factorial
from collections import defaultdict

A078698 = [1, 2, 20, 396, 14976, 907200, 79315200, 9551001600, 1513528934400,
           305106949324800, 76296489615360000, 23175289163980800000,
           8404709419090575360000, 3587225703492542791680000, 1779970753996760560435200000,
           1016036270188884847558656000000, 661106386935312429191528448000000]
A078702 = [1, 2, 13, 213, 7584, 454380, 39665160, 4775586480, 756765576000,
           152553490810560, 38148245068953600, 11587644586640707200,
           4202354709635579481600, 1793612851748170637184000, 889985376998423302704307200,
           508018135094443467957310848000, 330553193467656241628008759296000]


def A051286(n):
    return sum(comb(n - k, k) ** 2 for k in range(n // 2 + 1))


def lacings(n, ban):
    """all directed lacings 1 -> 2n under reading C (optionally without rule 2)."""
    N = 2 * n
    side = lambda e: e > n
    out = []

    def rec(p, used):
        if len(p) == N - 1:
            e = N
            if ban and p[-1] + e == N + 1:
                return
            if side(p[-2]) == side(p[-1]) == side(e):
                return
            out.append(tuple(p) + (e,))
            return
        for e in range(2, N):
            if used >> e & 1:
                continue
            if ban and p[-1] + e == N + 1:
                continue
            if len(p) >= 2 and side(p[-2]) == side(p[-1]) == side(e):
                continue
            p.append(e)
            rec(p, used | (1 << e))
            p.pop()
    rec([1], 2)
    return out


def mu(p, n):
    return tuple(2 * n + 1 - e for e in reversed(p))


print("1. literal enumeration, reading C")
for n in range(3, 7):          # n = 7 without the ban has 79e6 lacings: too many to list
    L0 = lacings(n, ban=False)
    fix0 = sum(1 for p in L0 if mu(p, n) == p)
    L1 = lacings(n, ban=True) if n <= 7 else None
    fix1 = sum(1 for p in L1 if mu(p, n) == p)
    S1 = set(L1)
    closed = all(mu(p, n) in S1 for p in L1)
    print(f"   n={n}: no ban: D'={len(L0)} (A078698={A078698[n-1]}, closed form {factorial(n-1)**2 * A051286(n)}), "
          f"mu-fixed={fix0} (2*A078702-A078698={2*A078702[n-1]-A078698[n-1]}) | with ban: D={len(L1)}, "
          f"mu-fixed={fix1}, mu-closed={closed}")


# 2. copy of method_dp/short.py transition with the rule-2 term removed
def D_noban(n):
    cur = {(n - 1, 0, 0, 0, 1, 0): 1}
    for _ in range(2 * (n - 1)):
        nxt = defaultdict(int)
        for (a, b, c, s, r, f), v in cur.items():
            for t in (0, 1):
                if t == s and r == 2:
                    continue
                q = r + 1 if t == s else 1
                if a:
                    key = (a - 1, b + 1, c) if t == 0 else (a - 1, b, c + 1)
                    nxt[key + (t, q, 1)] += a * v
                k = (c if t == 0 else b)            # rule 2 correction "- (f if t != s else 0)" removed
                if k > 0:
                    key = (a, b, c - 1) if t == 0 else (a, b - 1, c)
                    nxt[key + (t, q, 0)] += k * v
        cur = nxt
    return sum(v for (a, b, c, s, r, f), v in cur.items() if not (s == 1 and r == 2))


ok_data = all(D_noban(n) == A078698[n - 1] for n in range(3, 18))
ok_closed = all(D_noban(n) == factorial(n - 1) ** 2 * A051286(n) for n in range(3, 61))
print(f"2. method_dp transitions without rule 2: == A078698 data n=3..17: {ok_data}; == closed form n=3..60: {ok_closed}")


# 3. W(n) = number of admissible side words = A051286(n)
@lru_cache(maxsize=None)
def W(i, h, s, r, n):
    if i == n and h == n:
        return 1 if s == 1 else 0
    tot = 0
    for x in (0, 1):
        if x == s and r == 2:
            continue
        i2, h2 = i + (x == 0), h + (x == 1)
        if i2 <= n and h2 <= n:
            tot += W(i2, h2, x, r + 1 if x == s else 1, n)
    return tot
print("3. W(n) == A051286(n) for n=2..60:", all(W(1, 0, 0, 1, n) == A051286(n) for n in range(2, 61)))
