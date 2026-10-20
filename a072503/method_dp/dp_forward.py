#!/usr/bin/env python3
"""Forward profile DP for D(n) (one n at a time).  See METHOD.md, section 2-3.

State after placing the first t eyelets (t >= 1), as a dict key
    (a, b, c, s, r, f)
  a = # inner rows (rows 2..n) with neither eyelet used
  b = # inner rows with only the LEFT eyelet used
  c = # inner rows with only the RIGHT eyelet used
  s = side of the last placed eyelet (0 = left, 1 = right)
  r = length (1 or 2) of the current run of equal sides ending at the last eyelet
  f = 1 iff the partner (other eyelet of the same row) of the last placed eyelet
      is still unused (then it is forbidden as the next eyelet by rule 2)
Value = number of valid prefixes in that state.  The top row is handled outside
the classes: L1 is p_1 (initial state), R1 is p_{2n} (final step).
Usage: python3 dp_forward.py nmin nmax
"""
import sys
from collections import defaultdict

L, R = 0, 1


def D_forward(n):
    m = n - 1
    cur = {(m, 0, 0, L, 1, 0): 1}                 # p_1 = eyelet 1 (left, row 1)
    for _ in range(2 * m):                          # place the 2m inner eyelets
        nxt = defaultdict(int)
        for (a, b, c, s, r, f), v in cur.items():
            for s2 in (L, R):
                if s2 == s and r == 2:              # rule 3: would be 3 on one side
                    continue
                r2 = r + 1 if s2 == s else 1
                # (i) eyelet of an untouched row: a choices, partner now unused -> f=1
                if a:
                    key = (a - 1, b + 1, c, s2, r2, 1) if s2 == L else (a - 1, b, c + 1, s2, r2, 1)
                    nxt[key] += v * a
                # (ii) second eyelet of a half-used row; for side L these are the
                # c rows with only R used, for side R the b rows with only L used.
                # Rule 2 forbids the partner of the last eyelet: subtract f when
                # the side changes (then the last row is one of those rows).
                k = (c if s2 == L else b) - (f if s2 != s else 0)
                if k > 0:
                    key = (a, b, c - 1, s2, r2, 0) if s2 == L else (a, b - 1, c, s2, r2, 0)
                    nxt[key] += v * k
        cur = nxt
    # p_{2n} = eyelet 2n (right, row 1): forbidden only if it makes R,R,R.
    return sum(v for (a, b, c, s, r, f), v in cur.items()
               if (a, b, c) == (0, 0, 0) and not (s == R and r == 2))


if __name__ == "__main__":
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    for n in range(lo, hi + 1):
        D = D_forward(n)
        assert D % 2 == 0
        print(n, D, D // 2, flush=True)
