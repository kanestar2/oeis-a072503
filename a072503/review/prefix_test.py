#!/usr/bin/env python3
"""Test of method_dp's lumping lemma with its own production code.

For valid prefixes P = p_1..p_t (sampled at random, or all of them for small n),
count the valid completions of P by the reviewer's own memoized search over
(remaining eyelets, last eyelet, run flag) - no symmetry used - and compare with
F(profile(P)) read from the layers built by method_dp/dp_main.py (a COPY in
review/tmp/dp_copy; only next_layer/layer0/ix are used, main() is not run).

Usage: python3 -B prefix_test.py
"""
import os
import random
import sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tmp", "dp_copy"))
import dp_main  # noqa: E402

KMAX = 2 * (11 - 1)
LAYERS = [dp_main.layer0()]
for k in range(1, KMAX + 1):
    LAYERS.append(dp_main.next_layer(LAYERS[-1], k))


def F(a, b, c, s, r, f):
    k = 2 * a + b + c
    return int(LAYERS[k][a][dp_main.ix(s, r, f)][b])


def completions_factory(n):
    N = 2 * n
    side = lambda e: 0 if e <= n else 1

    @lru_cache(maxsize=None)
    def comp(rem, last, run):
        # rem: bitmask of unused inner eyelets (bit e); run: 1 or 2
        if rem == 0:
            if side(last) == 1 and run == 2:
                return 0                      # last two R and 2n is R
            if last + N == N + 1:
                return 0
            return 1
        tot = 0
        m = rem
        while m:
            e = (m & -m).bit_length() - 1
            m &= m - 1
            if e + last == N + 1:
                continue
            if side(e) == side(last):
                if run == 2:
                    continue
                tot += comp(rem & ~(1 << e), e, 2)
            else:
                tot += comp(rem & ~(1 << e), e, 1)
        return tot
    return comp


def profile(P, n):
    N = 2 * n
    used = set(P)
    a = b = c = 0
    for k in range(2, n + 1):
        l, r_ = k, N + 1 - k
        if l not in used and r_ not in used:
            a += 1
        elif l in used and r_ not in used:
            b += 1
        elif r_ in used and l not in used:
            c += 1
    side = lambda e: 0 if e <= n else 1
    last = P[-1]
    s = side(last)
    r = 2 if len(P) >= 2 and side(P[-2]) == s else 1
    f = 1 if last != 1 and (N + 1 - last) not in used else 0
    return a, b, c, s, r, f


def valid_prefix_random(n, t, rng):
    N = 2 * n
    side = lambda e: 0 if e <= n else 1
    while True:
        P = [1]
        ok = True
        while len(P) < t:
            cand = []
            for e in range(2, N):
                if e in P or e + P[-1] == N + 1:
                    continue
                if len(P) >= 2 and side(P[-2]) == side(P[-1]) == side(e):
                    continue
                cand.append(e)
            if not cand:
                ok = False
                break
            P.append(rng.choice(cand))
        if ok:
            return P


def all_prefixes(n, t):
    N = 2 * n
    side = lambda e: 0 if e <= n else 1
    out = []

    def rec(P):
        if len(P) == t:
            out.append(list(P))
            return
        for e in range(2, N):
            if e in P or e + P[-1] == N + 1:
                continue
            if len(P) >= 2 and side(P[-2]) == side(P[-1]) == side(e):
                continue
            P.append(e)
            rec(P)
            P.pop()
    rec([1])
    return out


def check(n, P, comp):
    N = 2 * n
    rem = 0
    for e in range(2, N):
        if e not in P:
            rem |= 1 << e
    side = lambda e: 0 if e <= n else 1
    run = 2 if len(P) >= 2 and side(P[-2]) == side(P[-1]) else 1
    mine = comp(rem, P[-1], run)
    theirs = F(*profile(P, n))
    return mine, theirs


if __name__ == "__main__":
    rng = random.Random(20261020)
    total = bad = 0
    # exhaustive: n = 4..6, every prefix length
    for n in (4, 5, 6):
        comp = completions_factory(n)
        cnt = 0
        for t in range(1, 2 * n):
            for P in all_prefixes(n, t):
                mine, theirs = check(n, P, comp)
                cnt += 1
                if mine != theirs:
                    bad += 1
                    if bad <= 10:
                        print("MISMATCH", n, P, mine, theirs)
        total += cnt
        # sum over all length-1 prefixes = D(n)
        print(f"exhaustive n={n}: {cnt} prefixes checked, D(n) from F = {F(n-1,0,0,0,1,0)}", flush=True)
    # random: n = 8..11, prefixes with at most 14 inner eyelets left
    for n in (8, 9, 10, 11):
        comp = completions_factory(n)
        cnt = 0
        for _ in range(300):
            tmin = max(2, 2 * n - 1 - 14)
            t = rng.randint(tmin, 2 * n - 1)
            P = valid_prefix_random(n, t, rng)
            mine, theirs = check(n, P, comp)
            cnt += 1
            if mine != theirs:
                bad += 1
                if bad <= 10:
                    print("MISMATCH", n, P, mine, theirs)
        total += cnt
        comp.cache_clear()
        print(f"random n={n}: {cnt} prefixes checked", flush=True)
    print(f"total {total} prefixes, mismatches {bad}")
    print("ALL OK" if bad == 0 else "FAILED")
