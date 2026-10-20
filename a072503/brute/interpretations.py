#!/usr/bin/env python3
"""Literal brute force over all permutations, testing several readings of the
'three eyelets' rule.  Pfoertner numbering: left side 1..n (top to bottom),
right side n+1..2n (bottom to top), horizontal pairs (k, 2n+1-k), top pair (1, 2n).

Usage: python3 interpretations.py NMAX
Counts directed lacings 1 -> 2n; the OEIS value is that count / 2.
"""
import sys
from itertools import permutations

def side(e, n):  return 0 if e <= n else 1
def row(e, n):   return e if e <= n else 2 * n + 1 - e

def rule_C(a, b, c, n):   # any three consecutive lace eyelets on one side
    return side(a, n) == side(b, n) == side(c, n)

def rule_B(a, b, c, n):   # three neighbouring eyelets of one column, in order
    if not (side(a, n) == side(b, n) == side(c, n)):
        return False
    ra, rb, rc = row(a, n), row(b, n), row(c, n)
    return (rb - ra == 1 and rc - rb == 1) or (ra - rb == 1 and rb - rc == 1)

def rule_A(a, b, c, n):   # three eyelets of one column, middle one between
    if not (side(a, n) == side(b, n) == side(c, n)):
        return False
    ra, rb, rc = row(a, n), row(b, n), row(c, n)
    return min(ra, rc) < rb < max(ra, rc)

RULES = {"A(in line, any gap)": rule_A, "B(in line, adjacent)": rule_B,
         "C(same side)": rule_C}

def count(n, triple_rule, forbid_horizontal=True, collect=False):
    N = 2 * n
    tot, found = 0, []
    for mid in permutations(range(2, N)):
        p = (1,) + mid + (N,)
        ok = True
        for i in range(N - 1):
            if forbid_horizontal and p[i] + p[i + 1] == N + 1:
                ok = False; break
        if ok:
            for i in range(N - 2):
                if triple_rule(p[i], p[i + 1], p[i + 2], n):
                    ok = False; break
        if ok:
            tot += 1
            if collect: found.append("".join(map(str, p)))
    return tot, found

if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    known = {3: 3, 4: 45, 5: 1824, 6: 109560}
    for name, r in RULES.items():
        for n in range(3, nmax + 1):
            t, f = count(n, r, collect=(n == 3))
            print(f"A072503 rule {name:22s} n={n}: directed={t} half={t/2} known={known.get(n)}"
                  + (f"  lacings={f}" if n == 3 else ""), flush=True)
    # sanity check of the 'in line' reading against A078602 (no horizontal ban)
    for name in ("A(in line, any gap)", "B(in line, adjacent)"):
        for n in (3, 4, 5):
            t, _ = count(n, RULES[name], forbid_horizontal=False)
            print(f"A078602 check rule {name}: n={n} -> {t} (A078602: 21, 601, 34278)", flush=True)
