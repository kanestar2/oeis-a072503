#!/usr/bin/env python3
"""Reviewer's test of alternative readings of the A072503 rules (own code).

Counts directed lacings p_1..p_2n (all eyelets once, Pfoertner numbering) under a
family of rule variants, by a memoized DFS over (used set, last two eyelets).
Compares D/2 (and D) with the OEIS terms a(3..9).

Usage: python3 alt_readings.py NMAX
"""
import sys
from functools import lru_cache

KNOWN = {3: 3, 4: 45, 5: 1824, 6: 109560, 7: 9520560, 8: 1145057760, 9: 181091917440}


def make(n, start_set, end_set, pair_ok, triple_ok):
    N = 2 * n
    full = (1 << (N + 1)) - 2

    @lru_cache(maxsize=None)
    def go(used, prev, last):
        if used == full:
            return 1 if last in end_set else 0
        tot = 0
        for e in range(1, N + 1):
            if used >> e & 1:
                continue
            if not pair_ok(last, e):
                continue
            if prev and not triple_ok(prev, last, e):
                continue
            # end eyelet must be last: if e is an allowed end and not the last one, fine;
            tot += go(used | (1 << e), last, e)
        return tot

    tot = 0
    for s in start_set:
        tot += go(1 << s, 0, s)
    go.cache_clear()
    return tot


def variants(n):
    N = 2 * n
    side = lambda e: 0 if e <= n else 1
    row = lambda e: e if e <= n else N + 1 - e
    horiz = lambda a, b: a + b == N + 1
    same3 = lambda a, b, c: side(a) == side(b) == side(c)
    V = {}
    # baseline = DEFINITION.md (reading C)
    V["C: start 1, end 2n, no horizontal, no 3 same side"] = (
        {1}, {N}, lambda a, b: not horiz(a, b), lambda a, b, c: not same3(a, b, c))
    V["C, but start/end at either top eyelet (both directions)"] = (
        {1, N}, {1, N}, lambda a, b: not horiz(a, b), lambda a, b, c: not same3(a, b, c))
    V["strict zigzag: no same-side step at all"] = (
        {1}, {N}, lambda a, b: not horiz(a, b) and side(a) != side(b), lambda a, b, c: True)
    V["C + no vertical neighbour step (k -> k+-1 same side)"] = (
        {1}, {N}, lambda a, b: not horiz(a, b) and not (side(a) == side(b) and abs(row(a) - row(b)) == 1),
        lambda a, b, c: not same3(a, b, c))
    V["C, but bottom pair (n, n+1) horizontal allowed"] = (
        {1}, {N}, lambda a, b: not (horiz(a, b) and row(a) != n), lambda a, b, c: not same3(a, b, c))
    V["C without the horizontal ban"] = (
        {1}, {N}, lambda a, b: True, lambda a, b, c: not same3(a, b, c))
    V["no horizontal, no 3-rule"] = (
        {1}, {N}, lambda a, b: not horiz(a, b), lambda a, b, c: True)
    V["C + no two consecutive same-side steps with same direction (A-like)"] = (
        {1}, {N}, lambda a, b: not horiz(a, b),
        lambda a, b, c: not (same3(a, b, c) and min(row(a), row(c)) < row(b) < max(row(a), row(c))))
    V["no 4 on one side (runs <= 3) + no horizontal"] = None   # handled separately
    return V


def count_run_cap(n, cap):
    """no horizontal, runs of equal sides <= cap, start 1 end 2n."""
    N = 2 * n
    side = lambda e: 0 if e <= n else 1
    full = (1 << (N + 1)) - 2

    @lru_cache(maxsize=None)
    def go(used, last, run):
        if used == full:
            return 1 if last == N else 0
        tot = 0
        for e in range(2, N + 1):
            if used >> e & 1 or last + e == N + 1:
                continue
            if e == N and used | (1 << e) != full:
                continue
            r2 = run + 1 if side(e) == side(last) else 1
            if r2 > cap:
                continue
            tot += go(used | (1 << e), e, r2)
        return tot
    return go(2, 1, 1)


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    names = [k for k in variants(3) if variants(3)[k] is not None]
    for name in names:
        row_out = []
        for n in range(3, nmax + 1):
            st, en, po, to = variants(n)[name]
            D = make(n, st, en, po, to)
            row_out.append(D)
        halves = [D / 2 for D in row_out]
        match = all(row_out[i] == 2 * KNOWN[i + 3] for i in range(len(row_out)))
        print(f"{name:72s} D={row_out}  match(D/2 = a)={match}", flush=True)
    rc = [count_run_cap(n, 3) for n in range(3, nmax + 1)]
    print(f"{'runs <= 3 (no 4 on one side) + no horizontal':72s} D={rc}  match={all(rc[i] == 2*KNOWN[i+3] for i in range(len(rc)))}")
    print("OEIS 2*a(n):", [2 * KNOWN[n] for n in range(3, nmax + 1)])
