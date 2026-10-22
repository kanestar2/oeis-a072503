#!/usr/bin/env python3
"""Reviewer's independent fast count of D(n) (no project code is used).

Derivation (global inclusion-exclusion over "glued" inner rows):
  For a set S of inner rows (rows 2..n), let A(S) = number of orderings with
  p_1 = 1, p_2n = 2n, no three consecutive on one side (rule 3), in which the two
  eyelets of every row in S are consecutive (rule 2 violated on purpose).
  Then D(n) = sum_S (-1)^|S| A(S)  (row 1 can never be glued: its eyelets are at
  positions 1 and 2n).  A(S) depends on j = |S| only.  Write the side word
  w (w_1 = L, w_2n = R, n letters each, no LLL/RRR).  The glued rows occupy j
  pairwise disjoint "dominoes" (t, t+1) with w_t != w_{t+1}, 2 <= t, t+1 <= 2n-1.
  Given w and the j dominoes: j! ways to put the rows of S on the dominoes
  (orientation is forced by w), (n-1-j)! ways for the remaining left positions
  (except position 1), (n-1-j)! for the remaining right positions (except 2n).
  With N_n(j) = sum_w #(sets of j such dominoes):
      D(n) = sum_j (-1)^j C(n-1,j) j! (n-1-j)!^2 N_n(j)
           = (n-1)! sum_j (-1)^j (n-1-j)! N_n(j).
N_n(j) is computed by a DP that reads the side word LETTER BY LETTER:
  state after t letters: (#L, side of letter t, run length 1/2, covered flag =
  "position t is the 2nd cell of a domino, or t = 1"), value = polynomial in y
  (y marks dominoes), packed in one Python int with B bits per coefficient.
  B = 4*NMAX + 8 is safe: a coefficient is at most (#words of length <= 2NMAX)
  * (#domino sets) <= 2^(2NMAX) * 2^(2NMAX).
For each n the last letter (position 2n, an R, never in a domino) is added
separately, so one pass serves all n <= NMAX.

Usage: python3 glue_ie.py NMAX OUTFILE      writes "n D(n) a(n)" lines, n = 2..NMAX
"""
import sys
import time
from math import factorial

L, R = 0, 1


def run(NMAX, out):
    B = 4 * NMAX + 8
    mask = (1 << B) - 1
    # layer: dict  i (#L) -> list of 8 packed polys indexed by s*4 + (r-1)*2 + c
    def idx(s, r, c):
        return s * 4 + (r - 1) * 2 + c
    layer = {1: [0] * 8}
    layer[1][idx(L, 1, 1)] = 1          # position 1 = eyelet 1 (left), covered
    t = 1
    t0 = time.time()
    fh = open(out, "w")
    fact = [factorial(k) for k in range(NMAX + 1)]
    while t < 2 * NMAX - 1:
        # ---- final step for n with 2n-1 == t:  cell (#L = n, #R = n-1)
        if t % 2 == 1:
            n = (t + 1) // 2
            if n >= 2 and n in layer:
                P = layer[n]
                tot = 0
                for s in (L, R):
                    for r in (1, 2):
                        if s == R and r == 2:      # R R + final R would be RRR
                            continue
                        for c in (0, 1):
                            tot += P[idx(s, r, c)]
                Nj = []
                while tot:
                    Nj.append(tot & mask)
                    tot >>= B
                S = sum((-1) ** j * fact[n - 1 - j] * v for j, v in enumerate(Nj))
                D = fact[n - 1] * S
                assert D % 2 == 0
                fh.write(f"{n} {D} {D // 2}\n")
                fh.flush()
        # ---- extend every prefix of length t by one letter (position t+1)
        new = {}
        for i, P in layer.items():
            h = t - i
            for s in (L, R):
                for r in (1, 2):
                    for c in (0, 1):
                        v = P[idx(s, r, c)]
                        if not v:
                            continue
                        for x in (L, R):
                            if x == s and r == 2:  # rule 3
                                continue
                            i2 = i + (x == L)
                            h2 = h + (x == R)
                            if i2 > NMAX or h2 > NMAX - 1:   # cannot reach (n, n-1), n <= NMAX
                                continue
                            r2 = r + 1 if x == s else 1
                            Q = new.get(i2)
                            if Q is None:
                                Q = new[i2] = [0] * 8
                            Q[idx(x, r2, 0)] += v                  # no domino on (t, t+1)
                            if x != s and c == 0:                  # domino on (t, t+1)
                                Q[idx(x, r2, 1)] += v << B
        layer = new
        t += 1
        if t % 100 == 0:
            print(f"t={t} elapsed {time.time() - t0:.1f}s", flush=True)
    # final step for n = NMAX (t = 2NMAX-1)
    n = NMAX
    P = layer.get(n)
    tot = 0
    for s in (L, R):
        for r in (1, 2):
            if s == R and r == 2:
                continue
            for c in (0, 1):
                tot += P[idx(s, r, c)]
    Nj = []
    while tot:
        Nj.append(tot & mask)
        tot >>= B
    D = fact[n - 1] * sum((-1) ** j * fact[n - 1 - j] * v for j, v in enumerate(Nj))
    assert D % 2 == 0
    fh.write(f"{n} {D} {D // 2}\n")
    fh.close()
    print(f"done NMAX={NMAX} in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python3 glue_ie.py NMAX OUTFILE")
    run(int(sys.argv[1]), sys.argv[2])
